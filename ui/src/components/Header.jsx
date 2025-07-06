import {
  Toolbar,
  ToolbarDivider,
  ToolbarButton,
  ToolbarGroup,
  Text,
  Avatar,
} from '@fluentui/react-components';
import {
  Home24Regular,
  Settings24Regular,
  Person24Regular,
  Navigation24Regular,
} from '@fluentui/react-icons';
import { useSidebarStore } from '../store/sidebarStore';

export const Header = () => {
  const toggleSidebar = useSidebarStore((state) => state.toggleSidebar);

  return (
    <header className="bg-white border-b border-gray-200 px-6 h-16 flex items-center justify-between">
      <div className="flex items-center gap-3">
        <ToolbarButton
          appearance="subtle"
          icon={<Navigation24Regular />}
          aria-label="Toggle sidebar"
          className="p-2 hover:bg-gray-100 rounded-md"
          onClick={toggleSidebar}
        />
        <Text className="text-xl font-semibold text-gray-800">IRR</Text>
      </div>
      
      <Toolbar className="flex items-center gap-2">
        <ToolbarGroup className="flex items-center gap-1">
          <ToolbarButton
            appearance="subtle"
            icon={<Home24Regular />}
            aria-label="Home"
          >
            Home
          </ToolbarButton>
          <ToolbarButton
            appearance="subtle"
            icon={<Settings24Regular />}
            aria-label="Settings"
          >
            Settings
          </ToolbarButton>
        </ToolbarGroup>
        
        <ToolbarDivider />
        
        <ToolbarGroup className="flex items-center gap-1">
          <ToolbarButton
            appearance="subtle"
            icon={<Person24Regular />}
            aria-label="Profile"
          >
            Profile
          </ToolbarButton>
          <Avatar 
            name="User"
            size={32}
            aria-label="User avatar"
            className="ml-2"
          />
        </ToolbarGroup>
      </Toolbar>
    </header>
  );
};