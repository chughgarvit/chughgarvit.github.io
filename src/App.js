import { useContext, useEffect } from 'react'
import AOS from "aos"
import Header from './components/Header/Header'
import About from './components/About/About'
import Projects from './components/Projects/Projects'
import Skills from './components/Skills/Skills'
import ScrollToTop from './components/ScrollToTop/ScrollToTop'
import Contact from './components/Contact/Contact'
import Footer from './components/Footer/Footer'
import Publications from './components/Publications/Publications'
import './App.css'
import "aos/dist/aos.css";
import { ThemeContext } from './contexts/theme'
import Achievements from './components/Achievements/Achievements'
import Education from './components/Timeline/Timeline'

require('dotenv').config()


const App = () => {
  const [{ themeName }] = useContext(ThemeContext)

  useEffect(() => {
    AOS.init();
    AOS.refresh();
  }, []);

  return (
    <div id='top' className={`${themeName} app`}>
      <Header />

      <main>
        <About />
        <Education />
        <Publications />
        <Achievements />
        <Projects />
        <Skills />
        <Contact />
      </main>

      <ScrollToTop />
      <Footer />
    </div>
  )
}

export default App
