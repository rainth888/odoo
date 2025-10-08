# task202509300922-bus-serialize-error-on-reload

Summary
- During server reload, a transient PostgreSQL serialization failure occurred on `bus_presence` when websockets terminated and tried to mark presence `offline` concurrently.

Details (from log)
- Query: UPDATE bus_presence ... could not serialize access due to concurrent update
- Stack: addons/bus/websocket.py during `_terminate()` commit/flush.

Impact
- Typically harmless; the presence row update is retried by other requests or expires. No business data loss.
- May drop one websocket connection during reload; clients reconnect automatically.

Mitigation / What to do
- If seen only during reload: ignore. Do a full restart instead of hot reload if you want to avoid it.
- After module updates, hard-reload the POS UI to re-establish websockets.
- If frequent outside reloads:
  - Check multiple workers doing concurrent presence writes.
  - Avoid overlapping reloads; serialize deploy steps.
  - Consider upgrading to latest Odoo minor where bus fixes may exist.

Verification
- Confirm POS chat/notifications/order sync still works after refresh.
- Monitor logs; error should not repeat constantly.

Follow-ups (optional)
- Add retry wrapper where appropriate (custom code) if your flow updates presence explicitly.
- Add health check for bus longpoll/websocket in your ops scripts.
