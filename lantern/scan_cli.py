import asyncio
from prompt_toolkit import Application,prompt
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.dimension import Dimension
from prompt_toolkit.layout import Layout,HSplit,Window
from prompt_toolkit.widgets import TextArea,Label,Box
from lantern.scan import get_live_devices,start_scan
from lantern.mdns import set_display_name

def device_list():
    devices=get_live_devices()
    lines=[]
    lines.append(f"----- Devices on Network (Live Refresh) -----")
    if not devices:
        lines.append("No devices available.")
    else:
        lines.append(f"{'Name':<12} {'IP Address':<15} {'Status'}")
        lines.append("-" * 40)
        for dev in devices:
            lines.append(f"{dev['name']:<12} {dev['ip']:<15} {dev['status']}")
    return "\n".join(lines)

async def run_scan_prompt_toolkit():
    start_scan()
    stop_event=asyncio.Event()
    device_panel=TextArea(height=Dimension(weight=1),focusable=False,read_only=True,dont_extend_height=True)
    console_text="lanshare>"
    console_panel=TextArea(height=Dimension(weight=1),scrollbar=True,focus_on_click=True,text=console_text,dont_extend_height=True)
    layout=Layout(HSplit([Box(height=Dimension(weight=1),body=device_panel,padding=0),Window(height=1,char='-'),Label("Type 'exit' to leave to the lanShare CLI and 'help' for list of commands\n"),Box(body=console_panel,padding=0,height=Dimension(weight=1))]))
    console_panel.buffer.cursor_position=len(console_panel.text)
    kb=KeyBindings()
    safe_pos=[0]
    @kb.add('enter')
    def handle_enter(event):
        nonlocal console_text
        lines=console_panel.text.strip().splitlines()
        last_line=lines[-1].strip()
        command=last_line[9:].strip()
        
        if command=="exit":
            stop_event.set()
            event.app.exit()
        elif command=="rename" or last_line=="r":
            console_text+=f"{command}\nRename not defined yet"
        elif command=="help":
            console_text+="\n'start': Start mDNS service (register your device on LAN) in the background.\n'rename': Change your display name and restart mDNS.\n'exit': To exit from 'scan' mode"
        else:
            console_text+=f"{command}\nCommand not Defined"
        console_text+="\nlanshare>"
        console_panel.text=console_text
        safe_pos[0]=len(console_panel.text)
        
        console_panel.buffer.cursor_position=len(console_panel.text)
    @kb.add('c-c')
    def handle_(event):
        stop_event.set()
        event.app.exit()
    @kb.add('backspace')
    def _(event):
        buffer = event.app.current_buffer
        if buffer.cursor_position > safe_pos[0]:
            buffer.delete_before_cursor()
    @kb.add("up")
    @kb.add("down")
    def _(event):
        pass
    @kb.add("left")
    def _(event):
        buffer=event.app.current_buffer
        if buffer.cursor_position>safe_pos[0]:
            buffer.cursor_position -=1
    
    app=Application(layout=layout,full_screen=True,key_bindings=kb)

    async def update_output():
        while not stop_event.is_set():
            device_panel.text=device_list()
            await asyncio.sleep(2)
    update_task=asyncio.create_task(update_output())
    await app.run_async()
    stop_event.set()
    await update_task
 