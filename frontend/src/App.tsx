import { BrowserRouter, Routes, Route } from 'react-router'
import { Refine } from '@refinedev/core'
import dataProvider from '@refinedev/simple-rest'
import { ThemeProvider } from '@/providers/ThemeProvider'
import { Layout } from '@/components/Layout'
import { HomePage } from '@/pages/HomePage'
import { NotasPage } from '@/pages/NotasPage'
import { FinanzasPage } from '@/pages/FinanzasPage'
import { ListasPage } from '@/pages/ListasPage'
import { CalendarioPage } from '@/pages/CalendarioPage'
import { ServiciosPage } from '@/pages/ServiciosPage'
import { AkiraPage } from '@/pages/AkiraPage'

const API_URL = '/api'

function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <Refine dataProvider={dataProvider(API_URL)}>
          <Routes>
            <Route element={<Layout />}>
              <Route path="/" element={<HomePage />} />
              <Route path="/notas" element={<NotasPage />} />
              <Route path="/finanzas" element={<FinanzasPage />} />
              <Route path="/listas" element={<ListasPage />} />
              <Route path="/calendario" element={<CalendarioPage />} />
              <Route path="/servicios" element={<ServiciosPage />} />
              <Route path="/akira" element={<AkiraPage />} />
            </Route>
          </Routes>
        </Refine>
      </BrowserRouter>
    </ThemeProvider>
  )
}

export default App
