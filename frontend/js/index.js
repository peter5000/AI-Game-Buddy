/*
  Skeleton JavaScript file
 */
'use strict';
(function() {
  window.addEventListener('load', init);

  /**
   * Initialize eventListners
   */
  function init() {

  }

  /**
   * Helper function to return the response's result text if successful, otherwise
   * returns the rejected Promise result with an error status and corresponding text
   * @param {object} res - response to check for success/error
   * @return {object} - valid response if response was successful, otherwise rejected
   *                    Promise result
   */
  async function statusCheck(res) {
    if (!res.ok) {
      throw new Error(await res.text());
    }
    return res;
  }

  /**
   *  Wrapper function for getElementById
   * @param {string} id - id for DOM element
   * @returns {HTMLElement} - DOM object with a given id
   */
  function id(id) {
    return document.getElementById(id);
  }

  /**
   *  Wrapper function for querySelector
   * @param {string} selector - CSS selector for DOM element
   * @returns {HTMLElement} - DOM object matching the given selector
   */
  function qs(selector) {
    return document.querySelector(selector);
  }

  /**
   *  Wrapper function for querySelectorAll
   * @param {string} selector - CSS selector for DOM elements
   * @returns {NodeList} - NodeList of DOM objects matching the given selector
   */
  function qsa(selector) {
    return document.querySelectorAll(selector);
  }

  /**
   * Wrapper function for a createElement
   *
   * @param {string} tag - html tag to create an html element
   * @returns {HTMLElement} - new DOM object with a given tag
   */
  function gen(tag) {
    return document.createElement(tag);
  }
})();