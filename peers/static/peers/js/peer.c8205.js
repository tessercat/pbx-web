/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = "./src/js/peer/index.js");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./src/js/logger.js":
/*!**************************!*\
  !*** ./src/js/logger.js ***!
  \**************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/*
 *  Copyright (c) 2020 Peter Christensen. All Rights Reserved.
 *  CC BY-NC-ND 4.0.
 */
function logPrefix() {
  if (!document.pbxLogPrefix) {
    const pbxScript = document.querySelector('#pbx-client-script');
    if (pbxScript) {
      document.pbxLogPrefix = pbxScript.src.split('/').pop().split('.')[0];
    } else {
      document.pbxLogPrefix = 'pbx-client';
    }
  }
  return `[${document.pbxLogPrefix} ${new Date().toLocaleTimeString()}]`;
}

let logger = {
  debug: (...args) => {
    if (document.debugLogEnabled) {
      console.debug(logPrefix(), ...args);
    }
  },
  verto: (...args) => {
    if (document.vertoLogEnabled) {
      console.log(logPrefix(), ...args);
    }
  },
  info: (...args) => {
    if (document.infoLogEnabled) {
      console.log(logPrefix(), ...args);
    }
  },
  error: (...args) => {
    console.error(logPrefix(), ...args);
  }
}
/* harmony default export */ __webpack_exports__["default"] = (logger);


/***/ }),

/***/ "./src/js/peer/index.js":
/*!******************************!*\
  !*** ./src/js/peer/index.js ***!
  \******************************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var webrtc_adapter__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! webrtc-adapter */ "webrtc-adapter");
/* harmony import */ var webrtc_adapter__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(webrtc_adapter__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _peer_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./peer.js */ "./src/js/peer/peer.js");
/*
 *  Copyright (c) 2020 Peter Christensen. All Rights Reserved.
 *  CC BY-NC-ND 4.0.
 */



document.debugLogEnabled = false;
document.vertoLogEnabled = true;
document.infoLogEnabled = true;

if (webrtc_adapter__WEBPACK_IMPORTED_MODULE_0___default.a.browserDetails.browser.startsWith("Not")) {
  alert("Your browser is not supported.");
} else {
  window.addEventListener('load', function () {
    document.peer = new _peer_js__WEBPACK_IMPORTED_MODULE_1__["default"]();
    document.peer.open();
  });
  window.addEventListener('beforeunload', function (event) {
    if (document.peer.snork) {
      event.preventDefault();
      event.returnValue = '';
    }
  });
  window.addEventListener('unload', function () {
    document.peer.close();
  });
}


/***/ }),

/***/ "./src/js/peer/peer.js":
/*!*****************************!*\
  !*** ./src/js/peer/peer.js ***!
  \*****************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return Peer; });
/* harmony import */ var _verto_client_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../verto/client.js */ "./src/js/verto/client.js");
/* harmony import */ var _logger_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../logger.js */ "./src/js/logger.js");
/*
 * Copyright (c) 2020 Peter Christensen. All Rights Reserved.
 * CC BY-NC-ND 4.0.
 */



const STATUS = {
  ready: 'ready',
  available: 'available',
  unavailable: 'unavailable',
  closed: 'closed'
}

const MESSAGES = {
  offer: 'offer',
  accept: 'accept',
  cancel: 'cancel',
  error: 'error'
}

class Peer {

  constructor() {
    this.client = new _verto_client_js__WEBPACK_IMPORTED_MODULE_0__["default"]();
    this.client.onReady = this._onReady.bind(this);
    this.client.onSub = this._onSub.bind(this);
    this.client.onPing = this._onPing.bind(this);
    this.client.onPunt = this._onPunt.bind(this);
    this.client.onEvent = this._onEvent.bind(this);
    this.client.onMessage = this._onMessage.bind(this);
  }

  // Verto client state

  close() {
    this.client.publish({
      peerStatus: STATUS.closed,
    });
    this.client.close();
  }

  open() {
    const sessionId = this.client.getSessionId();
    const url = `${location.href}/session?sessionId=${sessionId}`;
    fetch(url).then(response => {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error(response.status);
      }
    }).then(sessionData => {
      this.client.open(sessionData);
    }).catch(error => {
      if (error.message === '404') {
        const sessionId = this.client.getSessionId(true);
        const url = `${location.href}/session?sessionId=${sessionId}`;
        fetch(url).then(response => {
          if (response.ok) {
            return response.json();
          } else {
            throw new Error(response.status);
          }
        }).then(sessionData => {
          this.client.open(sessionData);
        }).catch(error => {
          _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].error(error);
        });
      } else {
        _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].error(error);
      }
    });
  }

  // Client callbacks

  _onReady() {
    this.client.subscribe();
  }

  _onSub() {
    this.client.publish({
      peerStatus: STATUS.ready,
      peerName: this.nameDialog.peerName
    });
  }

  _onPing() {
    this.client.publish({
      peerStatus: STATUS.available,
      peerName: this.nameDialog.peerName
    });
  }

  _onMessage(clientId, eventData) {
    const peerName = eventData.peerName;
    if (eventData.peerStatus === STATUS.available) {
      this._onAvailableMessage(clientId, peerName);
    } else if (eventData.peerAction === MESSAGES.offer) {
      this._onOfferMessage(clientId, peerName);
    } else if (eventData.peerAction === MESSAGES.accept) {
      this._onAcceptMessage(clientId, peerName);
    } else if (eventData.peerAction === MESSAGES.cancel) {
      this._onCancelMessage(clientId, peerName);
    } else if (eventData.peerAction === MESSAGES.error) {
      this._onErrorMessage(clientId, peerName);
    } else if ('candidate' in eventData) {
      this._onCandidateMessage(clientId, eventData);
    } else if ('sdp' in eventData) {
      this._onSdpMessage(clientId, eventData);
    } else {
      _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].error('Error handling message', clientId, eventData);
    }
  }

  _onEvent(clientId, eventData) {
    const peerName = eventData.peerName;
    if (eventData.peerStatus === STATUS.ready) {
      this._onReadyEvent(clientId, peerName);
    } else if (eventData.peerStatus === STATUS.available) {
      this._onAvailableEvent(clientId, peerName);
    } else if (eventData.peerStatus === STATUS.unavailable) {
      this._onUnavailableEvent(clientId, peerName);
    } else if (eventData.peerStatus === STATUS.closed) {
      this._onClosedEvent(clientId, peerName);
    } else {
      _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].error('Error handling event', clientId, eventData);
    }
  }

  _onPunt() {
    _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].info(
      'Offline. '
      + 'You\'re logged in from another tab '
      + 'or the channel is full.'
    );
  }

  // Verto message handlers

  _onAvailableMessage(clientId, peerName) {
    _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].info('Peer available message', clientId, peerName);
  }

  _onOfferMessage(clientId, peerName) {
    _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].info('Peer offer message', clientId, peerName);
  }

  _onAcceptMessage(clientId, peerName) {
    _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].info('Peer accept message', clientId, peerName);
  }

  _onCancelMessage(clientId, peerName) {
    _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].info('Peer cancel message', clientId, peerName);
  }

  _onErrorMessage(clientId, peerName) {
    _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].info('Peer error message', clientId, peerName);
  }

  _onCandidateMessage(clientId, candidate) {
    _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].info('Peer ICE message', clientId, candidate);
  }

  _onSdpMessage(clientId, sdp) {
    _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].info('Peer SDP message', clientId, sdp);
  }

  // Verto event handlers

  _onReadyEvent(clientId, peerName) {
    _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].info('Peer ready event', clientId, peerName);
  }

  _onAvailableEvent(clientId, peerName) {
    _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].info('Peer available event', clientId, peerName);
  }

  _onUnavailableEvent(clientId, peerName) {
    _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].info('Peer unavailable event', clientId, peerName);
  }

  _onClosedEvent(clientId, peerName) {
    _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].info('Peer closed event', clientId, peerName);
  }
}


/***/ }),

/***/ "./src/js/verto/client.js":
/*!********************************!*\
  !*** ./src/js/verto/client.js ***!
  \********************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return VertoClient; });
/* harmony import */ var _socket_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./socket.js */ "./src/js/verto/socket.js");
/* harmony import */ var _logger_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../logger.js */ "./src/js/logger.js");
/*
 * Copyright (c) 2020 Peter Christensen. All Rights Reserved.
 * CC BY-NC-ND 4.0.
 */



const CONST = {
  authRequired: -32000,
  pingInterval: 45,
  pingMaxDelay: 5,
  requestExpiry: 30,
}

class VertoRequest {
  constructor(sessionId, requestId, method, params) {
    this.jsonrpc = '2.0';
    this.id = requestId;
    this.method = method;
    this.params = {sessid: sessionId, ...params};
  }
}

class ResponseCallbacks {
  constructor(onSuccess, onError) {
    this.sent = new Date();
    this.onSuccess = onSuccess;
    this.onError = onError;
  }
}

class VertoClient {

  constructor(channelId) {
    this.channelId = channelId;
    this.channelData = this._getChannelData();
    this.sessionData = null;

    // Client state
    this.responseCallbacks = {};
    this.isAuthing = false;
    this.isAuthed = false;
    this.pingInterval = null;

    // Client event handlers
    this.onOpen = null;
    this.onClose = null;
    this.onLogin = null;
    this.onLoginError = null;
    this.onReady = null;
    this.onSub = null;
    this.onSubError = null;
    this.onPing = null;
    this.onPingError = null;
    this.onPunt = null;
    this.onEvent = null;
    this.onMessage = null;

    // Socket and event bindings
    this.socket = new _socket_js__WEBPACK_IMPORTED_MODULE_0__["default"]();
    this.socket.onOpen = this._onSocketOpen.bind(this);
    this.socket.onClose = this._onSocketClose.bind(this);
    this.socket.onMessage = this._onSocketMessage.bind(this);
  }

  // Public interface

  getSessionId(expired = false) {
    let sessionId = this._getVar('sessionId');
    if (expired || !sessionId) {
      sessionId = this._getUuid();
      this._setVar('sessionId', sessionId);
    }
    return sessionId;
  }

  open(sessionData) {
    this.sessionData = sessionData;
    this.socket.open();
  }

  close() {
    this.socket.close();
  }

  subscribe() {
    const onSuccess = () => {
      if (this.onSub) {
        this.onSub();
      } else {
        _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].verto('Subscribed');
      }
    }
    const onError = (error) => {
      if (this.onSubError) {
        this.onSubError(error);
      } else {
        _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].error('Subscription error', error);
      }
    }
    this._sendRequest('verto.subscribe', {
      eventChannel: this.channelId
    }, onSuccess, onError);
  }

  publish(eventData, onSuccess, onError) {
    _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].verto('Publishing event', eventData);
    const encoded = this._encode(eventData);
    if (encoded) {
      const onRequestSuccess = (message) => {
        if ('code' in message.result) {
          if (onError) {
            onError(message);
          } else {
            _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].error('Publish event error', message);
          }
        } else {
          if (onSuccess) {
            onSuccess(message);
          } else {
            _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].verto('Published event', message)
          }
        }
      }
      this._sendRequest('verto.broadcast', {
        localBroadcast: true,
        eventChannel: this.channelId,
        eventData: encoded,
      }, onRequestSuccess, onError);
    } else {
      if (onError) {
        onError('Encoding error');
      } else {
        _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].error('Encoding error', eventData);
      }
    }
  }

  sendMessage(clientId, msgData, onSuccess, onError) {
    _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].verto('Sending message', clientId, msgData);
    const encoded = this._encode(msgData);
    if (encoded) {
      this._sendRequest('verto.info', {
        msg: {
          to: clientId,
          body: encoded
        }
      }, onSuccess, onError);
    } else {
      if (onError) {
        onError(msgData);
      }
    }
  }

  // Verto socket event handlers

  _onSocketOpen() {
    this._resetClientState();
    if (this.onOpen) {
      this.onOpen();
    } else {
      _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].verto('Socket open');
    }
    this._sendRequest('login');
  }

  _onSocketClose() {
    this._resetClientState();
    this.sessionData = null;
    if (this.onClose) {
      this.onClose();
    } else {
      _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].verto('Socket closed');
    }
  }

  _onSocketMessage(event) {
    const message = this._parse(event.data);
    if (this.responseCallbacks[message.id]) {
      _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].debug('Received response', message);
      this._handleResponse(message);
    } else {
      _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].debug('Received event', message);
      this._handleEvent(message);
    }
  }

  // Client state helpers

  _cleanResponseCallbacks() {
    const expired = [];
    const now = new Date();
    _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].verto('Cleaning callbacks');
    for (const requestId in this.responseCallbacks) {
      const diff = now - this.responseCallbacks[requestId].sent;
      if (diff > CONST.requestExpiry * 1000) {
        expired.push(requestId);
      }
    }
    for (const requestId of expired) {
      delete this.responseCallbacks[requestId];
      _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].error('Deleted callback', requestId);
    }
  }

  _resetClientState() {
    this.isAuthing = false;
    this.isAuthed = false;
    clearInterval(this.pingInterval);
    this._cleanResponseCallbacks();
  }

  _getChannelData() {
    const channelData = JSON.parse(localStorage.getItem(this.channelId));
    if (channelData) {
      return channelData;
    }
    return {};
  }

  _getUuid() {
    const url = URL.createObjectURL(new Blob());
    URL.revokeObjectURL(url);
    return url.split('/').pop();
  }

  _getVar(key) {
    return this.channelData[key] || null;
  }

  _setVar(key, value) {
    let changed = false;
    if (value && value !== this.channelData[key]) {
      changed = true;
      this.channelData[key] = value;
      _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].verto('Set', key);
    } else if (this.channelData[key] && !value) {
      changed = true;
      delete this.channelData[key];
      _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].verto('Unset', key);
    }
    if (changed) {
      localStorage.setItem(
        this.channelId, JSON.stringify(this.channelData)
      );
    }
    return changed;
  }

  _sendRequest(method, params, onSuccess, onError) {
    const request = new VertoRequest(
      this.sessionData.sessionId,
      this._getUuid(),
      method,
      params
    );
    this.responseCallbacks[request.id] = new ResponseCallbacks(
      onSuccess, onError
    );
    _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].debug('Sending request', request);
    this.socket.send(request);
  }

  _ping() {
    this._cleanResponseCallbacks();
    const onError = (message) => {
      if (this.onPingError) {
        this.onPingError(message);
      } else {
        _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].error('Ping failure', message);
      }
    }
    const onSuccess = () => {
      if (this.onPing) {
        this.onPing();
      } else {
        _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].verto('Ping success');
      }
    }
    this._sendRequest('echo', {}, onSuccess, onError);
  }

  _pingInterval() {
    const delay = Math.floor(
      Math.random() * (CONST.pingMaxDelay * 2 + 1)
    ) - CONST.pingMaxDelay;
    return (CONST.pingInterval + delay) * 1000;
  }

  _login() {
    if (this.isAuthing) {
      return;
    }
    this.isAuthing = true;
    this.isAuthed = false;
    const onSuccess = () => {
      this.isAuthing = false;
      this.isAuthed = true;
      this.setInterval(this._ping, this._pingInterval());
      if (this.onLogin) {
        this.onLogin();
      } else {
        _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].verto('Logged in');
      }
    };
    const onError = (event) => {
      if (this.socket.isOpen()) {
        this.close();
      } else {
        this._resetClientState();
      }
      if (this.onLoginError) {
        this.onLoginError(event.error.message);
      } else {
        _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].error('Login failed', event);
      }
    };
    this._sendRequest('login', {
      login: this.sessionData.clientId,
      passwd: this.sessionData.password
    }, onSuccess, onError);
  }

  // WebSocket message handlers

  _handleResponse(message) {
    if (message.result) {
      const onSuccess = this.responseCallbacks[message.id].onSuccess;
      if (onSuccess) {
        onSuccess(message);
      } else {
        _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].verto('Response', message);
      }
    } else {
      if (message.error) {
        const code = parseInt(message.error.code);
        if (code === CONST.authRequired) {
          this._login();
        } else {
          const onError = this.responseCallbacks[message.id].onError;
          if (onError) {
            onError(message);
          } else {
            _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].error('Error response', message);
          }
        }
      } else {
        _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].error('Bad response', message);
      }
    }
    delete this.responseCallbacks[message.id];
  }

  _handleEvent(event) {
    if (event.method === 'verto.clientReady') {
      if (this.onReady) {
        this.onReady(event.params);
      } else {
        _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].verto('Client ready', event.params);
      }
    } else if (event.method === 'verto.info') {
      if (
          event.params
          && event.params.msg
          && event.params.msg.to
          && event.params.msg.from
          && event.params.msg.body) {
        const msg = event.params.msg;
        const clientId = msg.to.split('@').shift();
        const message = this._decode(msg.body);
        if (clientId && clientId === this.sessionData.clientId) {
          if (this.onMessage) {
            this.onMessage(msg.from, message);
          } else {
            _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].verto('Message', event, message);
          }
        } else {
          _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].error('Other message', event, message);
        }
      } else {
        _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].error('Empty message', event);
      }
    } else if (event.method === 'verto.event') {
      if (
          event.params
          && event.params.sessid
          && event.params.sessid === this.sessionData.sessionId) {
        _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].verto('Own event', event);
      } else if (
          event.params
          && event.params.userid
          && event.params.eventChannel
          && event.params.eventData) {
        if (event.params.eventChannel === this.channelId) {
          const clientId = event.params.userid.split('@').shift();
          const eventData = this._decode(event.params.eventData);
          if (this.onEvent) {
            this.onEvent(clientId, eventData);
          } else {
            _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].verto('Event', clientId, eventData);
          }
        } else {
          _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].error('Other event', event);
        }
      } else {
        _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].error('Bad event', event);
      }
    } else if (event.method === 'verto.punt') {
      this.close();
      if (this.onPunt) {
        this.onPunt();
      } else {
        _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].verto('Punt');
      }
    } else {
      _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].error('Unhandled', event);
    }
  }

  // Event and message data processing helpers.

  /*
   * These methods eat exceptions.
   *
   * Parsing takes a stringified object as input and returns the object,
   * or null on error.
   *
   * Encoding takes an object as input and returns a Base64-encoded JSON
   * string, or an empty string on error.
   *
   * Decoding takes a Base64-encoded stringified object as input, decodes
   * it and returns the object, or null on error.
   */

  _parse(string) {
    try {
      return JSON.parse(string);
    } catch (error) {
      _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].error('Error parsing', string, error);
      return null;
    }
  }

  _encode(object) {
    try {
      const string = JSON.stringify(object);
      return btoa(encodeURIComponent(string).replace(
        /%([0-9A-F]{2})/g, (match, p1) => {
          return String.fromCharCode('0x' + p1);
        }
      ));
    } catch (error) {
      _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].error('Error encoding', object, error);
      return '';
    }
  }

  _decode(encoded) {
    try {
      const string = decodeURIComponent(
        atob(encoded).split('').map((c) => {
          return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join('')
      );
      return JSON.parse(string);
    } catch (error) {
      _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].error('Error decoding', encoded, error);
      return null;
    }
  }
}


/***/ }),

/***/ "./src/js/verto/socket.js":
/*!********************************!*\
  !*** ./src/js/verto/socket.js ***!
  \********************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return VertoSocket; });
/* harmony import */ var _logger_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../logger.js */ "./src/js/logger.js");
/*
 *  Copyright (c) 2020 Peter Christensen. All Rights Reserved.
 *  CC BY-NC-ND 4.0.
 */


class VertoSocket {

  constructor() {
    this.socket = null;
    this.isOpening = false;
    this.isHalted = true;
    this.retryCount = 0;
    this.retryBackoff = 5;
    this.retryMaxWait = 30;
    this.retryTimer = null;

    // Events bindings
    this.onOpen = null;
    this.onClose = null;
    this.onMessage = null;
  }

  _setRetryTimer() {
    let delay = this.retryCount * this.retryBackoff;
    if (delay > this.retryMaxWait) {
      delay = this.retryMaxWait;
    }
    if (delay) { // Adjust delay by +/- retryBackoff
      delay += (Math.floor(
        Math.random() * (this.retryBackoff * 2 + 1)
      ) - this.retryBackoff);
    }
    _logger_js__WEBPACK_IMPORTED_MODULE_0__["default"].verto(`Waiting ${delay}s after ${this.retryCount} tries`);
    this.retryTimer = setTimeout(() => {
      this.retryCount += 1;
      this.open();
    }, delay * 1000);
  }

  isOpen() {
    return this.socket && this.socket.readyState <= 1;
  }

  open() {
    if (this.isOpen() || this.isOpening) {
      return;
    }
    this.isOpening = true;
    this.isHalted = false;
    clearTimeout(this.retryTimer);
    const socket = new WebSocket(
      `wss://${location.host}${location.pathname}/verto`
    );
    socket.onopen = () => {
      if (this.isOpening) {
        this.isOpening = false;
        this.socket = socket;
        this.retryCount = 0;
        if (this.onOpen) {
          this.onOpen();
        } else {
          _logger_js__WEBPACK_IMPORTED_MODULE_0__["default"].verto('Socket open');
        }
      }
    }
    socket.onclose = () => {
      this.isOpening = false;
      this.socket = null;
      if (this.onClose) {
        this.onClose();
      } else {
        _logger_js__WEBPACK_IMPORTED_MODULE_0__["default"].verto('Socket closed');
      }
      if (!this.isHalted) {
        this._setRetryTimer();
      }
    }
    socket.onmessage = (event) => {
      if (this.onMessage) {
        this.onMessage(event);
      } else {
        _logger_js__WEBPACK_IMPORTED_MODULE_0__["default"].verto('Socket received message', event);
      }
    }
  }

  close() {
    this.isHalted = true;
    this.isOpening = false;
    clearTimeout(this.retryTimer);
    this.retryCount = 0;
    if (this.isOpen()) {
      this.socket.close();
    }
  }

  send(message) {
    if (this.socket && this.socket.readyState === 1) {
      this.socket.send(JSON.stringify(message));
    } else {
      _logger_js__WEBPACK_IMPORTED_MODULE_0__["default"].error('Error sending', message);
    }
  }
}


/***/ }),

/***/ "webrtc-adapter":
/*!**************************!*\
  !*** external "adapter" ***!
  \**************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = adapter;

/***/ })

/******/ });