import { Suspense, StrictMode, lazy } from 'react';

import ReactDOM from 'react-dom/client';
import './index.css';
import {
  createBrowserRouter,
  RouterProvider
} from 'react-router-dom';
import '@fontsource/cabin';


let Root = lazy(() => import('./routes/root'));
let Terms = lazy(() => import('./routes/terms'));
let CommunityGuidelines = lazy(() => import('./routes/community-guidelines'));


let router = createBrowserRouter([
  {
    path: '/',
    // TODO: complete fallback screen
    element: <Suspense fallback={<div>Loading...</div>}><Root /></Suspense>
  },
  {
    path: '/terms',
    element: <Suspense fallback={<div>Loading...</div>}><Terms /></Suspense>
  },
  {
    path: '/community-guidelines',
    element: <Suspense fallback={<div>Loading...</div>}><CommunityGuidelines /></Suspense>
  }
]);


ReactDOM.createRoot(document.getElementById('mount') as HTMLElement).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
);
