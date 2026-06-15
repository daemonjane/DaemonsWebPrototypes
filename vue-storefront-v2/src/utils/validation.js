/**
 * Check if a value is non‑empty (trims whitespace).
 * @param {string} value
 * @returns {boolean}
 */
export function isRequired(value) {
  return value.trim() !== ''
}

/**
 * Validate email format.
 * @param {string} value
 * @returns {boolean}
 */
export function isValidEmail(value) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)
}

/**
 * Validate a form object and return an errors object.
 * @param {object} form - { fieldName: value }
 * @param {object} rules - { fieldName: ['required' | 'email'] }
 * @returns {object} errors - { fieldName: string }
 */
export function validateForm(form, rules) {
  const errors = {}
  for (const field of Object.keys(rules)) {
    const value = form[field] || ''
    const fieldRules = rules[field]
    if (fieldRules.includes('required') && !isRequired(value)) {
      errors[field] = 'This field is required'
    }
    if (fieldRules.includes('email') && !isValidEmail(value)) {
      errors[field] = errors[field] || 'Valid email is required'
    }
  }
  return errors
}