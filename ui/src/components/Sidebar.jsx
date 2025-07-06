import { useSidebarStore } from '../store/sidebarStore';
import {
  Home24Regular,
  Settings24Regular,
  Person24Regular,
  Document24Regular,
  Folder24Regular,
} from '@fluentui/react-icons';

export const Sidebar = () => {
  const sidebarOpen = useSidebarStore((state) => state.sidebarOpen);

  if (!sidebarOpen) return null;

  return (
    <aside className="fixed left-0 top-16 h-full w-64 bg-white border-r border-gray-200 shadow-lg z-40">
      <nav className="p-4 space-y-2">
        <div className="mb-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Navigation</h2>
          
          <div className="space-y-1">
            <a
              href="#"
              className="flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-md transition-colors"
            >
              <Home24Regular />
              <span>Home</span>
            </a>
            
            <a
              href="#"
              className="flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-md transition-colors"
            >
              <Document24Regular />
              <span>Documents</span>
            </a>
            
            <a
              href="#"
              className="flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-md transition-colors"
            >
              <Folder24Regular />
              <span>Projects</span>
            </a>
            
            <a
              href="#"
              className="flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-md transition-colors"
            >
              <Settings24Regular />
              <span>Settings</span>
            </a>
            
            <a
              href="#"
              className="flex items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-md transition-colors"
            >
              <Person24Regular />
              <span>Profile</span>
            </a>
          </div>
        </div>
      </nav>
    </aside>
  );
};