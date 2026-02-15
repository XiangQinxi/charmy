import charmy as cm

window = cm.Window(size=(300, 160))

window.bind(
    "resize", lambda event: print(f"<{event.event_type}>: {event["width"]}x{event['height']}")
)
window.bind(
    "move", lambda event: print(f"<{event.event_type}>: {event["x_root"]}+{event['y_root']}")
)

print(window)

cm.mainloop()
