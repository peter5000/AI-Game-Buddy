# Frontend Documentation

This document provides an overview of the frontend codebase, including the framework, libraries, project structure, and file interactions.

## Framework and Libraries

The frontend is built using a modern and robust stack of technologies. Below is a list of the main frameworks and libraries used in this project.

### Main Technologies

- **Next.js 15**: As the core framework, Next.js structures the entire application. We leverage the App Router to create distinct, server-rendered routes like `/games`, `/profile`, and `/settings`. This improves performance and SEO.
- **React 19**: React is used to build the interactive and dynamic user interface. For example, the landing page is composed of React components like `Card` and `Button` to display featured game rooms and recent activity in a modular way.
- **TypeScript**: We use TypeScript throughout the project to ensure type safety. This is especially important for defining the props for our reusable components in `components/ui` and for typing the data fetched from the backend, reducing runtime errors.
- **Tailwind CSS**: Tailwind is used for all styling. It allows for rapid UI development by composing utility classes directly in the component files. An example is the gradient background on the landing page (`bg-gradient-to-br from-purple-50 to-blue-50`) and the styling of the `Button` components.

### Other Important Libraries

- **Radix UI**: This library provides the foundation for our accessible UI components located in `frontend/components/ui`. Components like `Dialog` for modals, `DropdownMenu` for navigation, and `Toast` for notifications are built on top of Radix primitives.
- **lucide-react**: Used for all icons in the application, ensuring a consistent visual style. You can see these icons on the landing page, such as `<Gamepad2 />` and `<Users />`, which make the UI more intuitive.
- **react-hook-form & zod**: This pair is used for managing user input and validation. For instance, the sign-up and login forms in the `/accounts` section will use `react-hook-form` to manage form state and `zod` to define the validation schema for user credentials.
- **@tanstack/react-query**: This library, initialized in `QueryProvider`, handles all asynchronous data fetching. It's used to fetch data for the "Featured Rooms" and "Recent Activity" sections on the landing page, providing caching, and automatic refetching.
- **Next-Themes**: Integrated via the `ThemeProvider` in the root layout, this library enables the light and dark mode functionality across the application.

## Project Structure

The frontend codebase is organized into several directories, each with a specific purpose. This structure helps to keep the code organized and maintainable.

- **`app/`**: This is the most important directory in the project. It contains all the routes, pages, and layouts for the application, following the Next.js App Router conventions. Each folder inside this directory represents a route segment.
- **`components/`**: This directory contains reusable UI components that are used throughout the application. These components are designed to be modular and independent, making them easy to use and maintain.
- **`hooks/`**: This directory contains custom React hooks that encapsulate reusable logic. This helps to keep the components clean and focused on their presentation.
- **`lib/`**: This directory contains utility functions, helper scripts, and other shared code that doesn't fit into the other categories.
- **`public/`**: This directory is used to store static assets that are publicly accessible, such as images, fonts, and other files.
- **`styles/`**: This directory contains global styles and CSS files that are used throughout the application.

## File Interactions

The frontend follows a clear and modular architecture. The `Navbar` component (`frontend/components/navbar.tsx`) provides an excellent example of how different parts of the application interact.

### `Navbar` Component Breakdown

The `Navbar` is a client-side component (`"use client"`) that handles the main navigation. Here's how it connects to other parts of the codebase:

- **Routing**: It uses Next.js's `<Link>` component for client-side navigation to pages like `/games` and `/ai-friends`. For programmatic navigation, such as after a user signs out, it uses the `useRouter` hook.

- **Authentication and Data Fetching**:
    - It uses the custom `useAuth` hook (`frontend/hooks/use-auth.ts`) to determine if a user is authenticated.
    - Based on the authentication status, it uses `@tanstack/react-query`'s `useQuery` hook to fetch user data via the `getCurrentUser` function from `frontend/lib/api.ts`.
    - This demonstrates how components consume global context provided by `QueryProvider` and a likely `AuthProvider`.

- **Component Composition**:
    - The `Navbar` is a high-level component that is included in the root layout (`app/layout.tsx`), making it visible on all pages.
    - It is built by composing smaller, reusable UI components from `frontend/components/ui/`, such as `Button`, `DropdownMenu`, and `Avatar`. These UI components are built upon Radix UI primitives for accessibility and are styled with Tailwind CSS.

- **State Management**:
    - It uses React's `useState` hook to manage local UI state, such as the visibility of the mobile menu.
    - Global state, like the current user's data, is managed by `@tanstack/react-query`, which handles caching and refetching automatically.

This example illustrates the core architectural patterns of the application: a clear separation of concerns between pages, reusable components, and utility functions; a well-defined data flow using hooks and providers; and a modular approach to building the user interface.
