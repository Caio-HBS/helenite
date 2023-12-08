import { countries } from "country-list";

/**
 * Returns a boolean based on the value being a valid username or not.
 */
export function isValidName(value) {
  if (value.trim() === value) {
    const noWhitespaces = /^\S*$/;

    return noWhitespaces.test(value);
  }
  return false;
}

/**
 * Returns a boolean based on the value being a valid email or not.
 */
export function isEmail(value) {
  if (value.trim() === value) {
    const reEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    return reEmail.test(value);
  }
  return false;
}

/**
 * Returns a boolean based on the value being a valid slug or not.
 */
export function isSlug(value) {
  if (value.trim() === value) {
    const slugRegex = /^[a-z0-9-]+$/;

    return slugRegex.test(value);
  }
  return false;
}

/**
 * Returns a boolean based on the value being a valid date or not.
 */
export function isDate(value) {
  const regexDate = /^\d{4}-\d{2}-\d{2}$/;
  const noWhitespaces = value.trim() === value;

  return regexDate.test(value) && noWhitespaces;
}

/**
 * Returns a boolean based on the value being a valid country or not.
 */
export function isBirthplace(value) {
  if (value.trim() === value) {
    return countries.getName(value) !== null;
  }
  return false;
}

/**
 * Returns a boolean based on the value being a valid password or not.
 */
export function isValidPassword(value) {
  if (valor.length > 8 && value.trim() === value) {
    const hasLetter = /[a-zA-Z]/.test(value);
    const hasNum = /\d/.test(value);

    return hasLetter && hasNum;
  }
  return false;
}
