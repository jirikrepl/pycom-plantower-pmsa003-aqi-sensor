import React from 'react';
import { createStore } from 'redux'
import { createRoot } from 'react-dom/client';
import { Provider } from 'react-redux';
import App from './App';
import { QueryClient, QueryClientProvider } from 'react-query';
import { ReactQueryDevtools } from 'react-query/devtools';
import rootReducer from './reducers/index'

const queryClient = new QueryClient();
const container = document.getElementById('root')!;
const root = createRoot(container);
const store = createStore(rootReducer);

root.render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <Provider store={store}>
        <App />
      </Provider>
      <ReactQueryDevtools />
    </QueryClientProvider>
  </React.StrictMode>
);
