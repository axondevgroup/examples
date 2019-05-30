export const urlValidator: string = '\\b((http|https):\\/\\/?)[^\\s()<>]+(?:\\([\\w\\d]+\\)|([^[:punct:]\\s]|\\/?))';

export const nameValidation: RegExp = /[A-Za-z0-9]/;

export const fieldValidation: RegExp = /[A-Z_-]/;

export const rateValidation: string = '^[-+]?\\d*$';

export const onlyLiterals = /[a-zA-Z]/;

export const onlyNumbers = /[0-9]/;

export const packageAttachType = /[Per Unit]|[%]/;
