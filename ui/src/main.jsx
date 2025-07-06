import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { FluentProvider, webLightTheme } from '@fluentui/react-components';
import { ApolloProvider } from '@apollo/client'
import client from './lib/apollo'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <FluentProvider theme={webLightTheme}>
      <ApolloProvider client={client}>
        <App />
      </ApolloProvider>
    </FluentProvider>
  </StrictMode>,
)
