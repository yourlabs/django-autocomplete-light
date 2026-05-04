function regexQuote(str) {
  return (str + "").replace(/([\.\?\*\+\^\$\[\]\\\(\)\{\}\|\-])/g, "\\$1");
}

export default regexQuote;
