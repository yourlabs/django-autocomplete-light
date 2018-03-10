import accessibleAutocomplete from 'accessible-autocomplete'

const countries = [
  'France',
  'Germany',
  'United Kingdom'
]
alert('hi')
var select = document.querySelector('[data-autocomplete-light-function=accessible]')
accessibleAutocomplete({
  element: select,
  id: select.attrs.id, // To match it to the existing <label>.
  source: countries
})
