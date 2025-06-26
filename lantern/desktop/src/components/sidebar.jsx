import settings from '../assets/settings.svg'
import search from '../assets/search.svg'
import profile from '../assets/profile.svg'
function SidebarItem() {
    return (
        <div className='flex items-center justify-between mx-5 py-2 gap-2'>
            <div className='flex items-center gap-2'>
                <img src={profile} alt="profile" className='max-w-15' />
                <div className='flex flex-col items-center '>
                    <span className='text-start font-bold w-full text-lg'>John Doe</span>
                    <span className='text-start w-full text-ellipsis line-clamp-1'>You:Daa enthaan paruvadi busy aano</span>
                </div>
            </div>
            <div className='w-fit h-full'>
                <span className='text-end text-xs whitespace-nowrap w-fit'>7:38 AM</span>
            </div>
        </div>
    )
}
function Sidebar() {
    return (
        <div className="flex flex-col gap-1 flex-1 h-full bg-primary-color">
            <div id="sidebar-header" className="flex justify-between items-center m-5">
                <h1 className="text-3xl font-bold">Lantern</h1>
                <img src={settings} alt="settings" />
            </div>
            <div id="sidebar-search-bar" className="flex items-center justify-start mx-5 bg-secondary-color rounded-md p-2 gap-2">
                <img src={search} alt="search" />
                <input type="text" placeholder="Search" className="bg-transparent outline-none text-white" />
            </div>
            <div id="sidebar-body" className="flex flex-col gap-2 overflow-scroll">
                <SidebarItem />
                <SidebarItem />
                <SidebarItem />
                <SidebarItem />
                <SidebarItem />
                <SidebarItem />
                <SidebarItem />
                <SidebarItem />
                <SidebarItem />
            </div>
        </div>
    )
}

export default Sidebar;