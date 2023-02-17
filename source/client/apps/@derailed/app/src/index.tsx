/* @refresh reload */
import 'windi.css';

import { render } from 'solid-js/web';
import { Router } from '@solidjs/router';
import App from './app';

const thunder = document.getElementById('thunder');

render(
  () => (
    <Router>
      <App />
    </Router>
  ),
  thunder,
);
