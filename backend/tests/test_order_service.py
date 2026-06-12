import asyncio
import sys
from contextlib import asynccontextmanager
from datetime import date
from pathlib import Path

import pytest
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.db.base import Base
from app.db.enums import OrderStatus, RoomType
from app.db import models
from app.schemas import OrderCreate
from app.services import order as order_service


@asynccontextmanager
async def noop_redis_multi_lock(redis_client, keys):
    yield


async def noop_set_availability_cache(room_id, dates, is_available):
    return None


async def run_with_session(test_body):
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    try:
        async with session_factory() as session:
            role = models.Role(name="guest")
            user = models.User(
                name="Alice",
                phone_number="13800138000",
                identity_number="ID13800138000",
                hashed_password="hashed",
                role=role,
            )
            room = models.Room(
                room_number="A101",
                type_=RoomType.SINGLE,
                price=200.0,
            )
            session.add_all([role, user, room])
            await session.commit()
            await session.refresh(user)
            await session.refresh(room)

            return await test_body(session, user, room)
    finally:
        await engine.dispose()


def make_order_payload(room_id: int, check_in: date, check_out: date):
    return OrderCreate(
        name="Alice",
        phone_number="13800138000",
        room_id=room_id,
        check_in_date=check_in,
        check_out_date=check_out,
    )


def test_validate_transition_allows_configured_state_changes():
    cases = [
        (OrderStatus.PENDING, OrderStatus.CONFIRMED),
        (OrderStatus.PENDING, OrderStatus.CANCELLED_UNPAID),
        (OrderStatus.CONFIRMED, OrderStatus.CHECKED_IN),
        (OrderStatus.CONFIRMED, OrderStatus.CANCELLED_PAID),
        (OrderStatus.CHECKED_IN, OrderStatus.COMPLETED),
        (OrderStatus.CHECKED_IN, OrderStatus.REFUNDED),
        (OrderStatus.CANCELLED_PAID, OrderStatus.REFUNDED),
    ]

    for current_status, next_status in cases:
        order = models.Order(status=current_status)

        order_service.validate_transition(order, next_status)


def test_validate_transition_rejects_invalid_state_changes():
    cases = [
        (OrderStatus.PENDING, OrderStatus.CHECKED_IN),
        (OrderStatus.CANCELLED_UNPAID, OrderStatus.CONFIRMED),
        (OrderStatus.COMPLETED, OrderStatus.REFUNDED),
        (OrderStatus.REFUNDED, OrderStatus.CONFIRMED),
    ]

    for current_status, next_status in cases:
        order = models.Order(status=current_status)

        with pytest.raises(HTTPException) as exc_info:
            order_service.validate_transition(order, next_status)

        assert exc_info.value.status_code == 400


def test_create_order_deducts_inventory_for_each_stay_date(monkeypatch):
    monkeypatch.setattr(order_service, "redis_multi_lock", noop_redis_multi_lock)
    monkeypatch.setattr(order_service, "set_availability_cache", noop_set_availability_cache)

    async def scenario(session, user, room):
        payload = make_order_payload(
            room.id,
            check_in=date(2026, 7, 1),
            check_out=date(2026, 7, 4),
        )

        created = await order_service.create_order(session, payload, user)

        rows = (
            await session.execute(
                select(models.RoomAvailability).order_by(models.RoomAvailability.date)
            )
        ).scalars().all()

        assert created["status"] == OrderStatus.PENDING.value
        assert created["expense"] == 600.0
        assert [row.date for row in rows] == [
            date(2026, 7, 1),
            date(2026, 7, 2),
            date(2026, 7, 3),
        ]
        assert all(row.is_available is False for row in rows)
        assert all(row.order_id == created["id"] for row in rows)
        assert all(row.version == 1 for row in rows)

    asyncio.run(run_with_session(scenario))


def test_create_order_rejects_unavailable_inventory(monkeypatch):
    monkeypatch.setattr(order_service, "redis_multi_lock", noop_redis_multi_lock)
    monkeypatch.setattr(order_service, "set_availability_cache", noop_set_availability_cache)

    async def scenario(session, user, room):
        unavailable_day = models.RoomAvailability(
            room_id=room.id,
            date=date(2026, 7, 2),
            is_available=False,
            order_id=None,
            version=3,
        )
        session.add(unavailable_day)
        await session.commit()

        payload = make_order_payload(
            room.id,
            check_in=date(2026, 7, 1),
            check_out=date(2026, 7, 4),
        )

        with pytest.raises(HTTPException) as exc_info:
            await order_service.create_order(session, payload, user)

        orders = (await session.execute(select(models.Order))).scalars().all()
        rows = (await session.execute(select(models.RoomAvailability))).scalars().all()

        assert exc_info.value.status_code == 409
        assert orders == []
        assert len(rows) == 1
        assert rows[0].date == date(2026, 7, 2)
        assert rows[0].is_available is False
        assert rows[0].version == 3

    asyncio.run(run_with_session(scenario))


def test_cancel_pending_order_releases_inventory(monkeypatch):
    monkeypatch.setattr(order_service, "redis_multi_lock", noop_redis_multi_lock)
    monkeypatch.setattr(order_service, "set_availability_cache", noop_set_availability_cache)

    async def scenario(session, user, room):
        payload = make_order_payload(
            room.id,
            check_in=date(2026, 8, 10),
            check_out=date(2026, 8, 12),
        )
        created = await order_service.create_order(session, payload, user)

        cancelled = await order_service.cancel_order(session, created["id"], user)
        rows = (
            await session.execute(
                select(models.RoomAvailability).order_by(models.RoomAvailability.date)
            )
        ).scalars().all()

        assert cancelled["status"] == OrderStatus.CANCELLED_UNPAID.value
        assert [row.date for row in rows] == [date(2026, 8, 10), date(2026, 8, 11)]
        assert all(row.is_available is True for row in rows)
        assert all(row.order_id is None for row in rows)
        assert all(row.version == 2 for row in rows)

    asyncio.run(run_with_session(scenario))


def test_confirmed_order_can_check_in_and_check_out_releasing_inventory(monkeypatch):
    monkeypatch.setattr(order_service, "redis_multi_lock", noop_redis_multi_lock)
    monkeypatch.setattr(order_service, "set_availability_cache", noop_set_availability_cache)

    async def scenario(session, user, room):
        payload = make_order_payload(
            room.id,
            check_in=date(2026, 9, 20),
            check_out=date(2026, 9, 21),
        )
        created = await order_service.create_order(session, payload, user)

        confirmed = await order_service.confirm_order(session, created["id"], user)
        checked_in = await order_service.check_in_order(session, created["id"], user)
        checked_out = await order_service.check_out_order(session, created["id"], user)
        row = (
            await session.execute(select(models.RoomAvailability))
        ).scalar_one()

        assert confirmed["status"] == OrderStatus.CONFIRMED.value
        assert checked_in["status"] == OrderStatus.CHECKED_IN.value
        assert checked_out["status"] == OrderStatus.COMPLETED.value
        assert row.is_available is True
        assert row.order_id is None
        assert row.version == 2

    asyncio.run(run_with_session(scenario))
