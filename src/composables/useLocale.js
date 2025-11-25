import { ref, onMounted } from 'vue'

export default () => {
  const defaultLocale = 'en'
  const supported = ['en', 'fr', 'de', 'lë']
  const currentLocale = ref(defaultLocale)

  const initLocale = () => {
    const stored = localStorage.getItem('locale')
    if (stored && supported.includes(stored)) {
      currentLocale.value = stored
    } else {
      // try to use document language or navigator
      const docLang = document.documentElement.lang
      if (docLang && supported.includes(docLang)) {
        currentLocale.value = docLang
      } else if (navigator.language) {
        const short = navigator.language.split('-')[0]
        if (supported.includes(short)) currentLocale.value = short
      }
    }
    document.documentElement.lang = currentLocale.value
    localStorage.setItem('locale', currentLocale.value)
  }

  function setLocale(locale) {
    if (!supported.includes(locale)) return
    currentLocale.value = locale
    document.documentElement.lang = locale
    localStorage.setItem('locale', locale)
    // emit a custom event in case other parts of app want to react
    window.dispatchEvent(new CustomEvent('locale-changed', { detail: { locale } }))
  }

  onMounted(initLocale)

  return { currentLocale, setLocale, supported }
}
