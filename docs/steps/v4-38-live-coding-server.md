# V4-38: Live Coding Server

## Overview

Implement basic live coding server for real-time pattern manipulation.

## Objectives

1. Create WebSocket/OSC server
2. Handle real-time code evaluation
3. Manage pattern state
4. Support multiple users

## Implementation

```python
class LiveCodingServer:
    """Live coding server for real-time performance"""

    def __init__(self, host: str = "localhost", port: int = 8000):
        ...

    async def evaluate_pattern(
        self,
        code: str,
        session_id: str
    ) -> Pattern:
        """Evaluate pattern code"""

    async def broadcast_state(
        self,
        session_id: str,
        state: dict
    ):
        """Broadcast state to all clients"""
```

## Files to Create

- `src/musicgen/live/server.py`

## Success Criteria

- [ ] Server accepts connections
- [ ] Code evaluation working
- [ ] State synchronization working

## Next Steps

After completion, proceed to V4-39: Stream Based Rendering
