import { request } from "./http.js";
export async function createRoom(payload) {
    return request("/admins/room/", {
        method: "POST",
        body: JSON.stringify({
            ...payload,
            price: Number(payload.price),
        }),
        headers: {
            "Content-Type": "application/json",
        },
    });
}
//# sourceMappingURL=booking.js.map