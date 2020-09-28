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
/******/ 	return __webpack_require__(__webpack_require__.s = "./src/peer/index.js");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./src/client.js":
/*!***********************!*\
  !*** ./src/client.js ***!
  \***********************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return Client; });
/* harmony import */ var _websocket_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./websocket.js */ "./src/websocket.js");
/* harmony import */ var _logger_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./logger.js */ "./src/logger.js");
/*
 * Copyright (c) 2020 Peter Christensen. All Rights Reserved.
 * CC BY-NC-ND 4.0.
 */



const CONST = {
  authRequired: -32000,
  pingInterval: 45,
  pingMaxVary: 5,
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

class Client {

  constructor() {
    this.channelId = location.pathname.split('/').pop();
    this.ws = new _websocket_js__WEBPACK_IMPORTED_MODULE_0__["default"]();
    this.ws.onConnect = this._onWsConnect.bind(this);
    this.ws.onDisconnect = this._onWsDisconnect.bind(this);
    this.ws.onMessage = this._onWsMessage.bind(this);
    this.pingTimer = null;
    this.lastActive = null;
    this._addActivityListeners();
    this.currentRequestId = 0;
    this.authing = false;
    this.responseCallbacks = {};
    this.sessionData = this._initSessionData();
    this.isSubscribed = false;
    this.onConnect = () => {};
    this.onDisconnect = () => {};
    this.onLogin = () => {};
    this.onLoginError = () => {};
    this.onReady = () => {};
    this.onPing = () => {};
    this.onPingError = () => {};
    this.onPunt = () => {};
    this.onEvent = () => {};
    this.onMessage = () => {};
  }

  // Channel client interface.

  getSessionData(key) {
    return this.sessionData[key] || null;
  }

  setSessionData(key, value) {
    let changed = false;
    if (value && value !== this.sessionData[key]) {
      changed = true;
      this.sessionData[key] = value;
      _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].info('Set', key);
    } else if (this.sessionData[key] && !value) {
      changed = true;
      delete this.sessionData[key];
      _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].info('Unset', key);
    }
    if (changed) {
      localStorage.setItem(
        this.channelId, JSON.stringify(this.sessionData)
      );
    }
    return changed;
  }

  isConnected() {
    return this.ws.isConnected();
  }

  connect() {
    if (!this.isConnected()) {
      const onSuccess = (sessionId, loginData) => {
        this.sessionId = sessionId;
        this.clientId = loginData.clientId;
        this.password = loginData.password;
        this.ws.connect();
      };
      const onError = (error) => {
        this.onLoginError(error.message);
      }
      this._startSession(onSuccess, onError);
    }
  }

  disconnect() {
    this.onDisconnect();
    this.ws.disconnect();
  }

  subscribe(onSuccess, onError) {
    const onRequestSuccess = () => {
      this.isSubscribed = true;
      _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].info('Subscribed');
      if (onSuccess) {
        onSuccess();
      }
    }
    const onRequestError = (error) => {
      this.isSubscribed = false;
      _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].error('Subscription error', error);
      if (onError) {
        onError(error);
      }
    }
    this._sendRequest('verto.subscribe', {
      eventChannel: this.channelId
    }, onRequestSuccess, onRequestError);
  }

  publish(eventData, onSuccess, onError) {
    _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].client('Broadcast', eventData);
    const onRequestSuccess = (message) => {
      if ('code' in message.result) {
        if (onError) {
          onError(message);
        }
      } else {
        if (onSuccess) {
          onSuccess(message);
        }
      }
    }
    const encoded = this._encode(eventData);
    if (encoded) {
      this._sendRequest('verto.broadcast', {
        localBroadcast: true,
        eventChannel: this.channelId,
        eventData: encoded,
      }, onRequestSuccess, onError);
    } else {
      if (onError) {
        onError(eventData);
      }
    }
  }

  sendMessage(clientId, msgData, onSuccess, onError) {
    _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].client('Send', clientId, msgData);
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

  // Websocket event handlers.

  _onWsConnect() {
    _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].info('Connected');
    this.onConnect();
    this._cleanResponseCallbacks();
    this.lastActive = new Date();
    clearTimeout(this.pingTimer);
    this.pingTimer = setTimeout(() => {
      this._ping();
    }, this._pingInterval());
    this.authing = false;
    this._sendRequest('login');
  }

  _onWsDisconnect() {
    this.isSubscribed = false;
    clearTimeout(this.pingTimer);
    const isTimeout = this._isTimeout();
    this.lastActive = null;
    this.onDisconnect(isTimeout);
    if (isTimeout) {
      this.disconnect();
    }
    _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].info('Disconnected');
  }

  _onWsMessage(event) {
    const message = this._parse(event.data);
    if (this.responseCallbacks[message.id]) {
      _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].debug('Raw response', message);
      this._handleResponse(message);
    } else {
      _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].debug('Raw event', message);
      this._handleEvent(message);
    }
  }

  // Connection and session maintenance methods.

  _initSessionData() {
    return this.sessionData = JSON.parse(
      localStorage.getItem(this.channelId)
    ) || {};
  }

  _getSessionId(replace) {
    let sessionId = this.getSessionData('sessionId');
    if (replace || !sessionId) {
      const url = URL.createObjectURL(new Blob());
      URL.revokeObjectURL(url);
      sessionId = url.split('/').pop();
      this.setSessionData('sessionId', sessionId);
    }
    return sessionId;
  }

  _startSession(onSuccess, onError) {
    const sessionId = this._getSessionId();
    const url = `${location.href}/sessions?sessionId=${sessionId}`;
    fetch(url).then(response => {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error(response.status);
      }
    }).then(loginData => {
      onSuccess(sessionId, loginData);
    }).catch(error => {
      if (error.message === '404') {
        const sessionId = this._getSessionId(true);
        const url = `${location.href}/sessions?sessionId=${sessionId}`;
        fetch(url).then(response => {
          if (response.ok) {
            return response.json();
          } else {
            throw new Error(response.status);
          }
        }).then(loginData => {
          onSuccess(sessionId, loginData);
        }).catch(error => {
          onError(error);
        });
      } else {
        onError(error);
      }
    });
  }

  _cleanResponseCallbacks() {
    const expired = [];
    const now = new Date();
    _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].client('Cleaning callbacks');
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

  _sendRequest(method, params, onSuccess, onError) {
    this.currentRequestId += 1;
    const request = new VertoRequest(
      this.sessionId,
      this.currentRequestId,
      method,
      params
    );
    this.responseCallbacks[request.id] = new ResponseCallbacks(
      onSuccess, onError
    );
    _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].debug('Request', method, params);
    this.ws.send(request);
  }

  _login() {
    this.authing = true;
    const onSuccess = () => {
      _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].info('Logged in');
      this.authing = false;
      this.onLogin();
    };
    const onError = (event) => {
      _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].error('Login failed', event);
      this.disconnect();
      this.onLoginError(event.error.message);
    };
    this._sendRequest('login', {
      login: this.clientId,
      passwd: this.password
    }, onSuccess, onError);
  }

  _isTimeout() {
    if (this.lastActive) {
      const timeout = new Date(this.lastActive.getTime() + 60000);
      if (new Date() > timeout) {
        return true;
      }
    }
    return false;
  }

  _pingInterval() {
    const pingVary = Math.floor(
      Math.random() * (CONST.pingMaxVary * 2 + 1)
    ) - CONST.pingMaxVary;
    return (CONST.pingInterval + pingVary) * 1000;
  }

  _ping() {
    this._cleanResponseCallbacks();
    if (this.isConnected()) {
      if (this._isTimeout()) {
        this.disconnect();
      } else {
        const onError = (message) => {
          _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].error('Ping failed', message);
          this.onPingError(message);
        }
        const onSuccess = () => {
          clearTimeout(this.pingTimer);
          this.pingTimer = setTimeout(() => {
            this._ping();
          }, this._pingInterval());
          this.lastActive = new Date();
          this.onPing();
        }
        this._sendRequest('echo', {}, onSuccess, onError);
      }
    }
  }

  _addActivityListeners() {
    document.addEventListener('visibilitychange', () => {
      if (!document.hidden && this.isConnected()) {
        this._ping();
      }
    });
  }

  // Verto JSON-RPC response and event handlers.

  _handleResponse(message) {
    if (message.result) {
      const onSuccess = this.responseCallbacks[message.id].onSuccess;
      if (onSuccess) {
        onSuccess(message);
      }
    } else {
      if (message.error) {
        const code = parseInt(message.error.code);
        if (!this.authing && code === CONST.authRequired) {
          this._login();
        } else {
          const onError = this.responseCallbacks[message.id].onError;
          if (onError) {
            onError(message);
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
      _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].info('Ready');
      this.onReady();
    } else if (event.method === 'verto.info') {
      const msg = event.params.msg;
      if (msg) {
        const decoded = this._decode(msg.body);
        _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].client('Info', msg.from, decoded);
        this.onMessage(msg.from, decoded);
      } else {
        _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].error('Bad info', event);
      }
    } else if (event.method === 'verto.event') {
      if (event.params.sessid === this.sessionId) {
        return;
      }
      const clientId = event.params.userid.split('@').shift();
      const decoded = this._decode(event.params.eventData);
      _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].client('Event', clientId, decoded);
      this.onEvent(clientId, decoded);
    } else if (event.method === 'verto.punt') {
      _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].info('Punt');
      this.disconnect();
      this.onPunt(event);
    } else {
      _logger_js__WEBPACK_IMPORTED_MODULE_1__["default"].error('Bad event', event);
    }
  }

  // Event and message data processing helpers.

  /*
   * These methods eat exceptions. That's the point.
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

/***/ "./src/connection.js":
/*!***************************!*\
  !*** ./src/connection.js ***!
  \***************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return Connection; });
/* harmony import */ var _logger_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./logger.js */ "./src/logger.js");
/*
 * Copyright (c) 2020 Peter Christensen. All Rights Reserved.
 * CC BY-NC-ND 4.0.
 */


class Connection {

  constructor() {
    this.clientId = null;
    this.isPolite = null;
    this.userMedia = null;
    this.pc = null;
    this.makingOffer = false;
    this.ignoreOffer = false;
    this.onTrack = () => {};
    this.onSdp = () => {};
    this.onCandidate = () => {};
    this.onIceError = () => {};
  }

  isConnectedTo(clientId) {
    if (clientId && this.clientId) {
      return clientId === this.clientId;
    }
    return false;
  }

  isIdle() {
    return this.clientId === null;
  }

  init(clientId, isPolite, stunServer) {
    this.clientId = clientId;
    this.isPolite = isPolite;
    const configuration = {
      iceServers: [{urls: `stun:${stunServer}`}],
    }
    this.pc = new RTCPeerConnection(configuration);
    this.pc.ontrack = (event) => {
      if (event.track) {
        _logger_js__WEBPACK_IMPORTED_MODULE_0__["default"].info('Added remote', event.track.kind, 'track');
        this.onTrack(event.track);
      }
    };
    this.pc.onicecandidate = (event) => {
      if (event.candidate) {
        this.onCandidate(event.candidate.toJSON());
      } else {
        if (this.pc.connectionState === 'failed') {
          this.onIceError();
        }
      }
    };
    this.pc.onnegotiationneeded = async () => {
      try {
        this.makingOffer = true;
        const offer = await this.pc.createOffer();
        if (this.pc.signalingState !== 'stable') {
          _logger_js__WEBPACK_IMPORTED_MODULE_0__["default"].info('Abandoning SDP negotiation');
          return;
        }
        await this.pc.setLocalDescription(offer);
        if (this.pc.localDescription) {
          this.onSdp(this.pc.localDescription.toJSON());
        }
      } catch (error) {
        _logger_js__WEBPACK_IMPORTED_MODULE_0__["default"].error('SDP negotiation error', error);
      } finally {
        this.makingOffer = false;
      }
    };
  }

  open() {
    _logger_js__WEBPACK_IMPORTED_MODULE_0__["default"].info('Connecting');
    for (const track of this.userMedia.getTracks()) {
      this.pc.addTrack(track, this.userMedia);
    }
  }

  close() {
    this.clientId = null;
    if (this.pc) {
      this.pc.close();
      this.pc = null;
      _logger_js__WEBPACK_IMPORTED_MODULE_0__["default"].info('Connection closed');
    }
    if (this.userMedia) {
      for (const track of this.userMedia.getTracks()) {
        track.stop();
        _logger_js__WEBPACK_IMPORTED_MODULE_0__["default"].info('Stopped local', track.kind, 'track');
      }
      this.userMedia = null;
    }
  }

  // User media methods.

  initUserMedia(successHandler, errorHandler, audio, video) {
    const onSuccess = (stream) => {
      this.userMedia = stream;
      if (this.clientId) {
        successHandler();
      } else {

        /*
         * This runs when the connection closes while getUserMedia is
         * generating a local media stream.
         *
         * In September of 2020, there must be some kind of race condition
         * in Android Chromium (Android 10 Chrome, Android 6 Vivaldi)
         * when media stream tracks are stopped too soon after starting.
         *
         * Tracks are live before they're stopped, and ended after,
         * but stopping them so soon after starting must leave a reference
         * behind somewhere, because the browser shows media devices
         * as active, even after stream tracks close.
         *
         * A slight pause before stopping tracks seems to take care
         * of the problem.
         *
         * I haven't seen this in Firefox, Chromium or Vivaldi on Linux,
         * so I assume it's Android only.
         */

        const sleep = () => new Promise((resolve) => setTimeout(resolve, 500));
        sleep().then(() => {
          this.close();
        });
      }
    }
    const onError = (error) => {
      errorHandler(error);
    }
    this._getUserMedia(onSuccess, onError, audio, video);
  }

  _getUserMedia(onSuccess, onError, audio, video) {
    navigator.mediaDevices.enumerateDevices().then(devices => {
      let hasAudio = false;
      let hasVideo = false;
      for (const device of devices) {
        if (device.kind.startsWith('audio')) {
          _logger_js__WEBPACK_IMPORTED_MODULE_0__["default"].info('Found audio device');
          hasAudio = true;
        } else if (device.kind.startsWith('video')) {
          _logger_js__WEBPACK_IMPORTED_MODULE_0__["default"].info('Found video device');
          hasVideo = true;
        }
      }
      if (audio && !hasAudio) {
        throw new Error('No audio devices.');
      }
      if (video && !hasVideo) {
        throw new Error('No video devices.');
      }
      return navigator.mediaDevices.getUserMedia({audio, video});
    }).then(stream => {
      onSuccess(stream);
    }).catch(error => {
      onError(error);
    });
  }

  // Inbound signal handlers.

  async addCandidate(jsonCandidate) {
    if (this.pc.connectionState === 'failed') {
      this.onIceError();
    } else {
      try {
        await this.pc.addIceCandidate(jsonCandidate);
      } catch (error) {
        if (!this.ignoreOffer) {
          _logger_js__WEBPACK_IMPORTED_MODULE_0__["default"].error('Error adding remote candidate', error);
        }
      }
    }
  }

  async addSdp(jsonSdp, sdpHandler) {
    const sdp = new RTCSessionDescription(jsonSdp);
    const offerCollision = (
      sdp.type === 'offer'
      && (this.makingOffer || this.pc.signalingState !== 'stable')
    );
    this.ignoreOffer = !this.isPolite && offerCollision;
    if (this.ignoreOffer) {
      _logger_js__WEBPACK_IMPORTED_MODULE_0__["default"].info('Ignoring SDP offer');
      return;
    }
    if (offerCollision) {
      await Promise.all([
        this.pc.setLocalDescription({type: "rollback"}).catch((error) => {
          _logger_js__WEBPACK_IMPORTED_MODULE_0__["default"].error('SDP rollback error', error);
        }),
        this.pc.setRemoteDescription(sdp)
      ]);
      _logger_js__WEBPACK_IMPORTED_MODULE_0__["default"].info('Rolled back local SDP and accepted remote');
    } else {
      await this.pc.setRemoteDescription(sdp);
      _logger_js__WEBPACK_IMPORTED_MODULE_0__["default"].info('Accepted remote SDP');
    }
    if (sdp.type === 'offer') {
      await this.pc.setLocalDescription(await this.pc.createAnswer());
      sdpHandler(this.pc.localDescription.toJSON());
    }
  }
}


/***/ }),

/***/ "./src/logger.js":
/*!***********************!*\
  !*** ./src/logger.js ***!
  \***********************/
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
  client: (...args) => {
    if (document.clientLogEnabled) {
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

/***/ "./src/peer/help-dialog.js":
/*!*********************************!*\
  !*** ./src/peer/help-dialog.js ***!
  \*********************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return NameDialog; });
/*
 * Copyright (c) 2020 Peter Christensen. All Rights Reserved.
 * CC BY-NC-ND 4.0.
 */
const HELP_TEXT = [
  'Your phone, tablet or computer '
  + 'must have a camera and microphone installed and enabled. '
  + 'Make sure the browser has permission to use them.',
  'Check volume levels.',
  'Poor wireless is often the cause of poor quality calls.',
  'Connections fail when firewalls get in the way. '
  + 'Use a VPN when connecting to or from restrictive networks.',
  'Otherwise, the service should work between '
  + 'Firefox and Chromium-based browsers '
  + 'on Android, Windows and Linux, '
  + 'but it hasn\'t been tested on appleOS.'
]

class NameDialog {

  constructor(header) {
    this.section = this._section();
    this.footer = this._footer();
    this.modalContent = [header, this.section, this.footer];
    this.onClose = () => {};
  }

  _section() {
    const section = document.createElement('section');
    HELP_TEXT.forEach((line) => {
      const p = document.createElement('p');
      p.innerHTML = line;
      section.append(p);
    });
    return section;
  }

  _footer() {
    const closeButton = document.createElement('button');
    closeButton.setAttribute('title', 'Close this box');
    closeButton.textContent = 'Close';
    closeButton.style.float = 'right';
    closeButton.addEventListener('click', () => {
      this.onClose();
    });
    const footer = document.createElement('footer');
    footer.append(closeButton);
    return footer;
  }
}


/***/ }),

/***/ "./src/peer/index.js":
/*!***************************!*\
  !*** ./src/peer/index.js ***!
  \***************************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var webrtc_adapter__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! webrtc-adapter */ "webrtc-adapter");
/* harmony import */ var webrtc_adapter__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(webrtc_adapter__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _peer_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./peer.js */ "./src/peer/peer.js");
/*
 *  Copyright (c) 2020 Peter Christensen. All Rights Reserved.
 *  CC BY-NC-ND 4.0.
 */



if (webrtc_adapter__WEBPACK_IMPORTED_MODULE_0___default.a.browserDetails.browser.startsWith("Not")) {
  alert("Your browser is not supported.");
} else {
  window.addEventListener('load', function () {
    document.debugLogEnabled = false;
    document.clientLogEnabled = false;
    document.infoLogEnabled = true;
    document.peer = new _peer_js__WEBPACK_IMPORTED_MODULE_1__["default"]();
    document.peer.connect();
  });
  window.addEventListener('beforeunload', function (event) {
    if (!document.peer.connection.isIdle()) {
      event.preventDefault();
      event.returnValue = '';
    } else {
      document.peer.disconnect();
    }
  });
  window.addEventListener('unload', function () {
    document.peer.disconnect();
  });
}


/***/ }),

/***/ "./src/peer/name-dialog.js":
/*!*********************************!*\
  !*** ./src/peer/name-dialog.js ***!
  \*********************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return NameDialog; });
/*
 * Copyright (c) 2020 Peter Christensen. All Rights Reserved.
 * CC BY-NC-ND 4.0.
 */
class NameDialog {

  constructor(header) {
    this.peerId = null;
    this.section = this._section();
    this.footer = this._footer();
    this.modalContent = [header, this.section, this.footer];
    this.nameField = this.section.querySelector('#name-input');
    this.okButton = this.footer.querySelector('#name-ok');
    this.nameFieldValidator = new RegExp('^[a-zA-Z0-9]+( [a-zA-Z0-9]+)*$');
    this._addListeners();
    this.onSubmit = () => {};
    this.onClose = () => {};
  }

  setClientId(clientId) {
    this.peerId = clientId.substr(0, 5);
  }

  init(peerName) {
    this.nameField.value = peerName ? peerName : this.peerId;
    this.nameField.setCustomValidity('');
  }

  isValid(peerName) {
    if (this.nameFieldValidator.test(peerName) && peerName.length <= 32) {
      return true;
    }
    return false;
  }

  setFocus() {
    this.nameField.focus();
    this.nameField.select();
  }
  _section() {
    const input = document.createElement('input');
    input.setAttribute('type', 'text');
    input.setAttribute('id', 'name-input');
    const section = document.createElement('section');
    section.append(input);
    return section;
  }

  _footer() {
    const okButton = document.createElement('button');
    okButton.setAttribute('id', 'name-ok');
    okButton.setAttribute('title', 'Change your name');
    okButton.textContent = 'OK';
    okButton.style.float = 'right';
    okButton.addEventListener('click', () => {
      this._submit();
    });
    const closeButton = document.createElement('button');
    closeButton.setAttribute('title', 'Close this popup');
    closeButton.style.background = '#888';
    closeButton.textContent = 'Close';
    closeButton.addEventListener('click', () => {
      this.onClose();
    });
    const footer = document.createElement('footer');
    footer.append(okButton);
    footer.append(closeButton);
    return footer;
  }

  _addListeners() {
    this.nameField.addEventListener('keydown', (event) => {
      if (event.key === 'Enter' && this.nameField.validity.valid) {
        this._submit(this.onSubmit);
      }
    });
    this.nameField.addEventListener('input', () => {
      if (this.nameField.value === '') {
        this.nameField.setCustomValidity('');
        this.okButton.disabled = false;
      } else if (this.nameField.value === this.peerId) {
        this.nameField.setCustomValidity('')
        this.okButton.disabled = false;
      } else if (this.isValid(this.nameField.value)) {
        this.nameField.setCustomValidity('');
        this.okButton.disabled = false;
      } else {
        this.nameField.setCustomValidity('Up to 32 letters and spaces.');
        this.okButton.disabled = true;
      }
    });
  }

  _submit() {
    if (this.nameField.value === this.peerId) {
      this.onSubmit('');
    } else {
      this.onSubmit(this.nameField.value);
    }
  }
}


/***/ }),

/***/ "./src/peer/nav-menu.js":
/*!******************************!*\
  !*** ./src/peer/nav-menu.js ***!
  \******************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return NavMenu; });
/*
 * Copyright (c) 2020 Peter Christensen. All Rights Reserved.
 * CC BY-NC-ND 4.0.
 */
class NavMenu {

  constructor() {
    this.openHelpButton = this._openHelpButton();
    this.closeConnectionButton = this._closeConnectionButton();
    this.menu = null;
    this.onOpenHelp = () => {};
    this.onCloseConnection = () => {};
  }

  setOffline() {
    this.menu = this.openHelpButton;
  }

  setOnline() {
    this.menu = this.openHelpButton;
  }

  setConnected(clientId) {
    this.closeConnectionButton.clientId = clientId;
    this.menu = this.closeConnectionButton;
  }

  _openHelpButton() {
    const button = document.createElement('button');
    button.textContent = 'Help';
    button.classList.add('pseudo');
    button.setAttribute('title', 'Show help box');
    button.addEventListener('click', () => {
      this.onOpenHelp();
    });
    return button;
  }

  _closeConnectionButton() {
    const button = document.createElement('button');
    button.textContent = 'Close';
    button.classList.add('pseudo');
    button.setAttribute('title', 'Close the connection');
    button.addEventListener('click', () => {
      this.onCloseConnection(this.closeConnectionButton.clientId);
    });
    return button;
  }
}


/***/ }),

/***/ "./src/peer/nav-status.js":
/*!********************************!*\
  !*** ./src/peer/nav-status.js ***!
  \********************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return NavStatus; });
/*
 * Copyright (c) 2020 Peter Christensen. All Rights Reserved.
 * CC BY-NC-ND 4.0.
 */
class NavStatus {

  constructor() {
    this.nameButton = this._nameButton();
    this.peerLabel = this._peerLabel();
    this.menu = null;
    this.onOpen = () => {};
    this.getDisplayName = () => {'N/A'};
  }

  setClientId(clientId) {
    this.nameButton.peerId = clientId.substr(0, 5);
    this._initNameButton();
  }

  setPeerName(peerName) {
    this.nameButton.peerName = peerName;
    this._initNameButton();
  }

  setIdle() {
    this.menu = this.nameButton;
  }

  setConnected(clientId, peerName) {
    this.peerLabel.peerId = clientId.substr(0, 5);
    this.peerLabel.peerName = peerName;
    this._initPeerLabel();
    this.menu = this.peerLabel;
  }

  _nameButton() {
    const button = document.createElement('button');
    button.classList.add('pseudo');
    window.matchMedia(`(min-width: 480px)`).addListener(() => {
      this._initNameButton();
    });
    button.addEventListener('click', () => {
      this.onOpen();
    });
    return button;
  }

  _initNameButton() {
    if (this.nameButton.peerName) {
      this.nameButton.textContent = this.getDisplayName(
        this.nameButton.peerName, 480
      );
      this.nameButton.setAttribute(
        'title', `${this.nameButton.peerName} (${this.nameButton.peerId})`
      );
    } else {
      this.nameButton.textContent = this.nameButton.peerId;
      this.nameButton.setAttribute('title', 'Click to change your name');
    }
  }

  _peerLabel() {
    const label = document.createElement('label');
    label.classList.add('pseudo', 'button');
    window.matchMedia(`(min-width: 480px)`).addListener(() => {
      this._initPeerLabel();
    });
    return label;
  }

  _initPeerLabel() {
    if (this.peerLabel.peerName) {
      this.peerLabel.textContent = this.getDisplayName(
        this.peerLabel.peerName, 480
      );
      this.peerLabel.setAttribute(
        'title', `${this.peerLabel.peerName} (${this.peerLabel.peerId})`
      );
    } else {
      this.peerLabel.textContent = this.peerLabel.peerId;
      this.peerLabel.removeAttribute('title');
    }
  }
}


/***/ }),

/***/ "./src/peer/offer-dialog.js":
/*!**********************************!*\
  !*** ./src/peer/offer-dialog.js ***!
  \**********************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return ConnectDialog; });
/* harmony import */ var _logger_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../logger.js */ "./src/logger.js");
/*
 * Copyright (c) 2020 Peter Christensen. All Rights Reserved.
 * CC BY-NC-ND 4.0.
 */


class ConnectDialog {

  constructor() {
    this.section = document.createElement('section');
    this.footer = this._footer();
    this.modalContent = [this.section, this.footer];
    this.offerId = null;
    this.onCancel = () => {};
  }

  _footer() {
    const cancelButton = document.createElement('button');
    cancelButton.textContent = 'Cancel';
    cancelButton.setAttribute('title', 'Cancel the offer');
    cancelButton.style.float = 'right';
    cancelButton.addEventListener('click', () => {
      this.onCancel();
    });
    const footer = document.createElement('footer');
    footer.append(cancelButton);
    return footer;
  }

  isOffering() {
    return this.offerId !== null;
  }

  isOfferTo(peerId) {
    return peerId !== null && peerId === this.offerId;
  }

  setInitializing() {
    this.offerId = null;
    this.section.textContent = 'Starting local media.';
  }

  setOffering(peerId) {
    this.offerId = peerId;
    this.section.textContent = 'Offer sent. Waiting for a reply.';
  }

  setClosed(message) {
    this.offerId = null;
    if (message) {
      this.section.textContent = message;
      _logger_js__WEBPACK_IMPORTED_MODULE_0__["default"].info(message);
    }
  }
}


/***/ }),

/***/ "./src/peer/offers-dialog.js":
/*!***********************************!*\
  !*** ./src/peer/offers-dialog.js ***!
  \***********************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return OffersDialog; });
/* harmony import */ var _logger_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../logger.js */ "./src/logger.js");
/*
 * Copyright (c) 2020 Peter Christensen. All Rights Reserved.
 * CC BY-NC-ND 4.0.
 */


class OffersDialog {

  constructor(header) {
    this.header = header;
    this.panel = document.createElement('section');
    this.footer = document.createElement('footer');
    this.modalContent = [this.header, this.panel, this.footer];
    this.offers = {};
    this.ignored = {};
    this._setMatchMedia();
    this.onAccept = () => {};
    this.onIgnore = () => {};
    this.getDisplayName = () => {return 'N/A'};
  }

  _setMatchMedia() {
    matchMedia('(min-width: 480px)').addListener(() => {
      for (const clientId in this.offers) {
        this._setPeerName(this.offers[clientId]);
      }
    });
  }

  _setPeerName(offer) {
    if (offer.peerName) {
      offer.label.textContent = this.getDisplayName(offer.peerName, 480);
      offer.label.setAttribute(
        'title', `${offer.peerName} (${offer.peerId})`
      );
      offer.ignoreButton.setAttribute(
        'title', `Ignore offer from ${offer.peerName} (${offer.peerId})`
      );
      offer.acceptButton.setAttribute(
        'title', `Accept offer from ${offer.peerName} (${offer.peerId})`
      );
    } else {
      offer.label.textContent = this.getDisplayName(offer.peerId);
      offer.label.removeAttribute('title');
      offer.ignoreButton.setAttribute(
        'title', `Ignore offer from ${offer.peerId}`
      );
      offer.acceptButton.setAttribute(
        'title', `Accept offer from ${offer.peerId}`
      );
    }
  }

  hasOffers() {
    return Object.keys(this.offers).length > 0;
  }

  addOffer(clientId, peerName) {
    if (this.offers[clientId]) {
      this.offers[clientId].added = new Date();
      if (peerName !== this.offers[clientId].peerName) {
        this.offers[clientId].peerName = peerName;
        this._setPeerName(this.offers[clientId]);
      }
      return;
    }
    if (this.ignored[clientId]) {
      this.ignored[clientId].added = new Date();
      return;
    }
    const offer = document.createElement('article');
    offer.classList.add('card')
    const section = document.createElement('section');
    section.style.padding = '0.5em';
    offer.append(section);
    const label = document.createElement('label');
    label.textContent = peerName;
    label.classList.add('pseudo', 'button');
    section.append(label);
    const acceptButton = document.createElement('button')
    acceptButton.textContent = 'Connect';
    acceptButton.setAttribute('title', `Connect to ${peerName}`);
    acceptButton.style.float = 'right';
    acceptButton.style.marginLeft = '0.2em';
    acceptButton.addEventListener('click', () => {
      this.onAccept(clientId, this.offers[clientId].peerName);
    });
    section.append(acceptButton);
    const ignoreButton = document.createElement('button');
    ignoreButton.textContent = 'Ignore';
    ignoreButton.setAttribute('title', 'Ignore this offer');
    ignoreButton.style.float = 'right';
    ignoreButton.classList.add('warning');
    ignoreButton.addEventListener('click', () => {
      this.onIgnore(clientId);
    });
    section.append(ignoreButton);
    offer.added = new Date();
    offer.clientId = clientId;
    offer.peerId = clientId.substr(0, 5);
    offer.peerName = peerName;
    offer.ignoreButton = ignoreButton;
    offer.acceptButton = acceptButton;
    offer.label = label;
    this.offers[clientId] = offer;
    this._setPeerName(offer);
    this.panel.append(offer);
    _logger_js__WEBPACK_IMPORTED_MODULE_0__["default"].info('Received offer', clientId);
  }

  ignoreOffer(clientId) {
    if (this.ignored[clientId]) {
      this.ignored[clientId].added = new Date();
    } else {
      this.ignored[clientId] = {added: new Date()};
      _logger_js__WEBPACK_IMPORTED_MODULE_0__["default"].info('Ignored offer', clientId);
    }
  }

  removeOffer(clientId) {
    if (this.ignored[clientId]) {
      delete this.ignored[clientId];
      _logger_js__WEBPACK_IMPORTED_MODULE_0__["default"].info('Removed ignored offer', clientId);
    }
    if (this.offers[clientId]) {
      this.offers[clientId].remove();
      delete this.offers[clientId];
      _logger_js__WEBPACK_IMPORTED_MODULE_0__["default"].info('Removed offer', clientId);
    }
  }

  reset() {
    Object.keys(this.offers).forEach(clientId => {
      this.removeOffer(clientId);
    });
  }

  clean() {
    _logger_js__WEBPACK_IMPORTED_MODULE_0__["default"].debug('Cleaning expired offers');
    const expired = new Set();
    const now = new Date();
    for (const clientId in this.offers) {
      const diff = now - this.offers[clientId].added;
      if (diff > 60000) {
        expired.add(clientId);
      }
    }
    for (const clientId in this.ignored) {
      const diff = now - this.ignored[clientId].added;
      if (diff > 60000) {
        expired.add(clientId);
      }
    }
    for (const clientId of expired) {
      _logger_js__WEBPACK_IMPORTED_MODULE_0__["default"].info('Offer expired', clientId);
      this.removeOffer(clientId);
    }
  }
}


/***/ }),

/***/ "./src/peer/peer.js":
/*!**************************!*\
  !*** ./src/peer/peer.js ***!
  \**************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return Peer; });
/* harmony import */ var _client_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../client.js */ "./src/client.js");
/* harmony import */ var _connection_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../connection.js */ "./src/connection.js");
/* harmony import */ var _nav_status_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./nav-status.js */ "./src/peer/nav-status.js");
/* harmony import */ var _nav_menu_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./nav-menu.js */ "./src/peer/nav-menu.js");
/* harmony import */ var _help_dialog_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./help-dialog.js */ "./src/peer/help-dialog.js");
/* harmony import */ var _name_dialog_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./name-dialog.js */ "./src/peer/name-dialog.js");
/* harmony import */ var _peers_panel_js__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./peers-panel.js */ "./src/peer/peers-panel.js");
/* harmony import */ var _offers_dialog_js__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./offers-dialog.js */ "./src/peer/offers-dialog.js");
/* harmony import */ var _offer_dialog_js__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./offer-dialog.js */ "./src/peer/offer-dialog.js");
/* harmony import */ var _view_js__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../view.js */ "./src/view.js");
/* harmony import */ var _logger_js__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../logger.js */ "./src/logger.js");
/*
 * Copyright (c) 2020 Peter Christensen. All Rights Reserved.
 * CC BY-NC-ND 4.0.
 */












const STATUS = {
  ready: 'ready',
  available: 'available',
  unavailable: 'unavailable',
  gone: 'gone'
}

const MESSAGES = {
  offer: 'offer',
  accept: 'accept',
  close: 'close',
  error: 'error'
}

class Peer {

  constructor() {

    // Client
    this.client = new _client_js__WEBPACK_IMPORTED_MODULE_0__["default"]();
    this.client.onDisconnect = this._onDisconnect.bind(this);
    this.client.onLogin = this._onLogin.bind(this);
    this.client.onLoginError = this._onLoginError.bind(this);
    this.client.onReady = this._onReady.bind(this);
    this.client.onPing = this._onPing.bind(this);
    this.client.onPunt = this._onPunt.bind(this);
    this.client.onEvent = this._onEvent.bind(this);
    this.client.onMessage = this._onMessage.bind(this);

    // Connection
    this.connection = new _connection_js__WEBPACK_IMPORTED_MODULE_1__["default"]();

    // View
    this.view = new _view_js__WEBPACK_IMPORTED_MODULE_9__["default"]();

    // Nav status
    this.navStatus = new _nav_status_js__WEBPACK_IMPORTED_MODULE_2__["default"]();
    this.navStatus.getDisplayName = this._getDisplayName;
    this.navStatus.onOpen = this._showNameDialog.bind(this);

    // Nav menu
    this.navMenu = new _nav_menu_js__WEBPACK_IMPORTED_MODULE_3__["default"]();
    this.navMenu.setOffline();
    this.navMenu.onCloseConnection = this._onCloseConnection.bind(this);
    this.navMenu.onOpenHelp = this._onOpenHelp.bind(this);
    this.view.setNavMenu(this.navMenu.menu);

    // Help dialog
    this.helpDialog = new _help_dialog_js__WEBPACK_IMPORTED_MODULE_4__["default"](this.view.modalHeader('Troubleshooting'));
    this.helpDialog.onClose = this._onCloseHelp.bind(this);
    this.helpDialog.onModalEscape = this._onCloseHelp.bind(this);

    // NameDialog
    this.peerName = null;
    this.nameDialog = new _name_dialog_js__WEBPACK_IMPORTED_MODULE_5__["default"](this.view.modalHeader('Enter your name'));
    this.nameDialog.onSubmit = this._onSubmitName.bind(this);
    this.nameDialog.onClose = this._onCancelName.bind(this);
    this.nameDialog.onModalEscape = this._onCancelName.bind(this);

    // PeersPanel
    this.peersPanel = new _peers_panel_js__WEBPACK_IMPORTED_MODULE_6__["default"]();
    this.peersPanel.getDisplayName = this._getDisplayName;
    this.peersPanel.onOffer = this._onOffer.bind(this);
    this.view.setChannelInfo(this.peersPanel.info);

    // OfferDialog
    this.offerDialog = new _offer_dialog_js__WEBPACK_IMPORTED_MODULE_8__["default"]();
    this.offerDialog.onCancel = this._onCancelOffer.bind(this);
    this.offerDialog.onModalEscape = this._onCancelOffer.bind(this);

    // OffersDialog
    this.offersDialog = new _offers_dialog_js__WEBPACK_IMPORTED_MODULE_7__["default"](this.view.modalHeader('Offers'));
    this.offersDialog.getDisplayName = this._getDisplayName;
    this.offersDialog.onAccept = this._onAcceptOffer.bind(this)
    this.offersDialog.onIgnore = this._onIgnoreOffer.bind(this);
    this.offersDialog.hasModalContent = this.offersDialog.hasOffers;
  }

  connect() {
    this.client.connect();
  }

  disconnect() {
    this.client.disconnect();
  }

  // Callbacks and helpers.

  _getDisplayName(peerName, clipWidth) {
    if (peerName && window.innerWidth < clipWidth) {
      let parts = peerName.split(' ');
      if (parts[0].length > 8) {
        return `${parts[0].substring(0, 6)}..`
      }
      return parts[0];
    }
    if (peerName) {
      return peerName;
    }
    return 'N/A';
  }

  _showNameDialog() {
    this.nameDialog.init(this.peerName);
    this.view.showModal(this.nameDialog);
  }

  _subscribe() {
    const onPubSuccess = () => {
      this.navMenu.setOnline();
      this.view.setNavMenu(this.navMenu.menu);
      this.peersPanel.setOnline();
    };
    const onPubError = () => {
      this.view.showAlert('Channel access error');
      this.disconnect();
    }
    const onSubSuccess = () => {
      this.client.publish({
        peerStatus: STATUS.ready,
        peerName: this.peerName
      }, onPubSuccess, onPubError);
    };
    const onSubError = () => {
      this.view.showAlert('Subscription error');
      this.disconnect();
    }
    this.client.subscribe(onSubSuccess, onSubError);
  }

  _openConnection(clientId, peerName) {
    if (this.connection.isConnectedTo(clientId)) {
      this.connection.onTrack = (track) => {
        this.view.addTrack(track);
      };
      this.connection.onSdp = (sdp) => {
        this.client.sendMessage(clientId, sdp);
        _logger_js__WEBPACK_IMPORTED_MODULE_10__["default"].info('Sent SDP');
      };
      this.connection.onCandidate = (candidate) => {
        this.client.sendMessage(clientId, candidate);
        _logger_js__WEBPACK_IMPORTED_MODULE_10__["default"].info('Sent candidate');
      };
      this.connection.onIceError = () => {
        this.client.sendMessage(clientId, {peerAction: MESSAGES.error});
        this._closeConnection('ICE failed.');
        this.view.showAlert('ICE failed. Can\'t connect.');
        this.view.showModal(this.offersDialog);
        this.client.publish({
          peerStatus: STATUS.available,
          peerName: this.peerName
        });
      };
      this.navStatus.setConnected(clientId, peerName);
      this.view.setNavStatus(this.navStatus.menu);
      this.navMenu.setConnected(clientId);
      this.view.setNavMenu(this.navMenu.menu);
      this.connection.open();
    }
  }

  _closeConnection(...message) {
    _logger_js__WEBPACK_IMPORTED_MODULE_10__["default"].info(...message);
    this.view.hidePlayer();
    this.connection.close();
    this.navStatus.setIdle();
    this.view.setNavStatus(this.navStatus.menu);
    this.navMenu.setOnline();
    this.view.setNavMenu(this.navMenu.menu);
  }

  // Nav menu callbacks.

  _onCloseConnection(clientId) {
    this._closeConnection('Closing connection');
    this.client.sendMessage(clientId, {peerAction: MESSAGES.close});
    this.client.publish({
      peerStatus: STATUS.available,
      peerName: this.peerName
    });
    this.view.showModal(this.offersDialog);
  }

  // HelpDialog callbacks.

  _onCloseHelp() {
    this.view.hideModal(this.helpDialog);
  }

  _onOpenHelp() {
    this.view.showModal(this.helpDialog);
  }

  // NameDialog callbacks.

  _onSubmitName(peerName) {
    this.view.hideModal(this.nameDialog);
    this.peerName = peerName; // Validation in modal.
    this.navStatus.setPeerName(peerName);
    const changed = this.client.setSessionData('peerName', peerName);
    if (changed && this.client.isSubscribed && this.connection.isIdle()) {
      this.client.publish({
        peerStatus: STATUS.available,
        peerName: this.peerName
      });
    } else if (this.client.isConnected() && !this.client.isSubscribed) {
      this._subscribe();
    }
  }

  _onCancelName() {
    this.view.hideModal(this.nameDialog);
    if (!this.client.isSubscribed) {
      this._subscribe();
    }
  }

  // PeersPanel callbacks.

  _onOffer(clientId) {
    const onSuccess = () => {
      this.client.sendMessage(
        clientId, {peerAction: MESSAGES.offer, peerName: this.peerName}
      );
      this.client.publish({peerStatus: STATUS.unavailable});
      this.offerDialog.setOffering(clientId);
    };
    const onError = (error) => {
      _logger_js__WEBPACK_IMPORTED_MODULE_10__["default"].info('Error offering connection', error.message);
      this.offerDialog.setClosed();
      this.view.showAlert(error.message);
      this.view.showModal(this.offersDialog);
      this.connection.close();
    };
    if (this.connection.isIdle()) {
      _logger_js__WEBPACK_IMPORTED_MODULE_10__["default"].info('Offering connection', clientId);
      this.connection.init(clientId, true, location.hostname);
      this.offerDialog.setInitializing();
      this.view.showModal(this.offerDialog);
      this.connection.initUserMedia(onSuccess, onError, true, true);
    }
  }

  _onCancelOffer() {
    if (this.offerDialog.isOffering()) {
      _logger_js__WEBPACK_IMPORTED_MODULE_10__["default"].info('Canceling offer');
      this.client.sendMessage(
        this.offerDialog.offerId, {peerAction: MESSAGES.close}
      );
    }
    this.offerDialog.setClosed();
    this.view.hideModal(this.offerDialog);
    this.connection.close();
    this.client.publish(
      {peerStatus: STATUS.available, peerName: this.peerName}
    );
    this.view.showModal(this.offersDialog);
  }

  // OffersDialog callbacks.

  _onIgnoreOffer(clientId) {
    this.offersDialog.removeOffer(clientId);
    this.offersDialog.ignoreOffer(clientId);
    if (!this.offersDialog.hasOffers()) {
      this.view.hideModal(this.offersDialog);
    }
  }

  _onAcceptOffer(clientId, peerName) {
    const onSuccess = () => {
      this.client.sendMessage(
        clientId, {peerAction: MESSAGES.accept, peerName: this.peerName}
      );
      this.client.publish({peerStatus: STATUS.unavailable});
      this._openConnection(clientId, peerName);
      this.offersDialog.removeOffer(clientId);
    };
    const onError = (error) => {
      this.client.sendMessage(clientId, {peerAction: MESSAGES.error});
      this._closeConnection('Error accepting offer', clientId, error.message);
      this.view.showAlert(error.message);
      this.view.showModal(this.offersDialog);
      this.offersDialog.removeOffer(clientId);
    };
    if (this.connection.isIdle()) {
      _logger_js__WEBPACK_IMPORTED_MODULE_10__["default"].info('Accepted offer', clientId);
      this.view.showPlayer();
      this.view.hideModal(this.offersDialog);
      this.connection.init(clientId, false, location.hostname);
      this.connection.initUserMedia(onSuccess, onError, true, true);
    }
  }

  // Client callbacks.

  _onDisconnect(isTimeout) {
    if (this.client.isConnected()) {
      this.client.publish({peerStatus: STATUS.gone});
    } else {
      this.navMenu.setOffline();
      this.view.setNavMenu(this.navMenu.menu);
      this.peersPanel.setOffline();
      this.peersPanel.reset();
      this.offersDialog.reset();
      this.view.hideModal(this.offersDialog);
      if (this.offerDialog.isOffering()) {
        this.offerDialog.setClosed('You left the channel.');
      } else if (isTimeout) {
        this.view.showAlert(
          'Offline. '
          + 'The connection timed out. '
          + 'Reload the page to re-join the channel.'
        );
      }
    }
  }

  _onLogin() {
    this.navStatus.setClientId(this.client.clientId);
    this.nameDialog.setClientId(this.client.clientId);
  }

  _onLoginError(message) {
    this.view.showAlert(`Login failed. ${message}.`);
  }

  _onReady() {
    this.peerName = this.client.getSessionData('peerName');
    this.navStatus.setPeerName(this.peerName);
    this.navStatus.setIdle();
    this.view.setNavStatus(this.navStatus.menu);
    if (this.peerName) {
      this._subscribe();
    } else {
      this._showNameDialog();
    }
  }

  _onPing() {
    if (this.offerDialog.isOffering()) {
      this.client.sendMessage(
        this.offerDialog.offerId,
        {peerAction: MESSAGES.offer, peerName: this.peerName}
      );
    }
    if (this.connection.isIdle() && this.client.isSubscribed) {
      this.client.publish({
        peerStatus: STATUS.available,
        peerName: this.peerName
      });
    }
    const expired = this.peersPanel.clean();
    for (const clientId of expired) {
      if (this.offerDialog.isOfferTo(clientId)) {
        this.offerDialog.setClosed('The other peer left the channel.');
        break;
      }
    }
    this.offersDialog.clean();
    if (!this.offersDialog.hasOffers()) {
      this.view.hideModal(this.offersDialog);
    }
  }

  _onEvent(clientId, eventData) {
    if (eventData.peerStatus === STATUS.ready) {
      this._handleReady(clientId, eventData.peerName);
    } else if (eventData.peerStatus === STATUS.available) {
      this._handleAvailable(clientId, eventData.peerName);
    } else if (eventData.peerStatus === STATUS.unavailable) {
      this._handleUnavailable(clientId);
    } else if (eventData.peerStatus === STATUS.gone) {
      this._handleGone(clientId);
    } else {
      _logger_js__WEBPACK_IMPORTED_MODULE_10__["default"].error('Bad event', clientId, eventData);
    }
  }

  _onMessage(clientId, eventData) {
    if (eventData.peerAction === MESSAGES.offer) {
      this._handleOffer(clientId, eventData.peerName);
    } else if (eventData.peerAction === MESSAGES.accept) {
      this._handleAccept(clientId, eventData.peerName);
    } else if (eventData.peerAction === MESSAGES.close) {
      this._handleClose(clientId);
    } else if (eventData.peerAction === MESSAGES.error) {
      this._handleError(clientId);
    } else if (eventData.peerStatus === STATUS.available) {
      this._handleAvailable(clientId, eventData.peerName);
    } else if ('candidate' in eventData) {
      this._handleCandidate(clientId, eventData);
    } else if ('sdp' in eventData) {
      this._handleSdp(clientId, eventData);
    } else {
      _logger_js__WEBPACK_IMPORTED_MODULE_10__["default"].error('Bad message', clientId, eventData);
    }
  }

  _onPunt() {
    this.view.showAlert(
      'Offline. '
      + 'You\'re logged in from another tab '
      + 'or the channel is full.'
    );
  }

  // Client message/event handlers.

  _handleOffer(clientId, peerName) {
    if (!peerName || !this.nameDialog.isValid(peerName)) {
      peerName = '';
    }
    this.offersDialog.addOffer(clientId, peerName);
    if (this.connection.isIdle()) {
      this.view.showModal(this.offersDialog);
    }
  }

  _handleAccept(clientId, peerName) {
    if (this.connection.isConnectedTo(clientId)) {
      if (!peerName || !this.nameDialog.isValid(peerName)) {
        peerName = '';
      }
      this.view.showPlayer();
      this.offerDialog.setClosed();
      this.view.hideModal(this.offerDialog);
      this._openConnection(clientId, peerName);
    }
  }

  _handleClose(clientId) {
    if (this.offerDialog.isOfferTo(clientId)) {
      this.offerDialog.setClosed('The other peer rejected the offer.');
    } else if (this.connection.isConnectedTo(clientId)) {
      this._closeConnection('The other peer closed the connection', clientId);
      this.client.publish({
        peerStatus: STATUS.available,
        peerName: this.peerName
      });
      this.view.showModal(this.offersDialog);
    }
    this.offersDialog.removeOffer(clientId);
    if (!this.offersDialog.hasOffers()) {
      this.view.hideModal(this.offersDialog);
    }
  }

  _handleError(clientId) {
    if (this.connection.isConnectedTo(clientId)) {
      this._closeConnection('The other peer failed to connect', clientId);
      this.client.publish({
        peerStatus: STATUS.available,
        peerName: this.peerName
      });
      this.offerDialog.setClosed();
      this.view.showAlert('The other peer failed to connect.');
      this.view.showModal(this.offersDialog);
    }
  }

  _handleReady(clientId, peerName) {
    if (!peerName || !this.nameDialog.isValid(peerName)) {
      peerName = '';
    }
    this.offersDialog.removeOffer(clientId);
    if (!this.offersDialog.hasOffers()) {
      this.view.hideModal(this.offersDialog);
    }
    this.peersPanel.addPeer(clientId, peerName);
    if (this.connection.isIdle()) {
      this.client.sendMessage(
        clientId, {
          peerStatus: STATUS.available,
          peerName: this.peerName
        }
      );
    }
  }

  _handleAvailable(clientId, peerName) {
    if (!peerName || !this.nameDialog.isValid(peerName)) {
      peerName = '';
    }
    this.peersPanel.addPeer(clientId, peerName);
  }

  _handleUnavailable(clientId) {
    this.peersPanel.removePeer(clientId);
  }

  _handleGone(clientId) {
    if (this.offerDialog.isOfferTo(clientId)) {
      this.offerDialog.setClosed('The other peer left the channel.');
    }
    if (this.connection.isConnectedTo(clientId)) {
      this._closeConnection('The other peer left the channel', clientId);
    }
    this.peersPanel.removePeer(clientId);
    this.offersDialog.removeOffer(clientId);
    if (!this.offersDialog.hasOffers()) {
      this.view.hideModal(this.offersDialog);
    }
  }

  _handleCandidate(clientId, candidate) {
    if (this.connection.isConnectedTo(clientId)) {
      _logger_js__WEBPACK_IMPORTED_MODULE_10__["default"].info('Received candidate');
      this.connection.addCandidate(candidate).then(() => {
      }).catch(error => {
        _logger_js__WEBPACK_IMPORTED_MODULE_10__["default"].error('Error adding candidate', error);
      });
    }
  }

  _handleSdp(clientId, sdp) {
    if (this.connection.isConnectedTo(clientId)) {
      _logger_js__WEBPACK_IMPORTED_MODULE_10__["default"].debug('Received SDP');
      const sdpHandler = (newJsonSdp) => {
        this.client.sendMessage(clientId, newJsonSdp);
        _logger_js__WEBPACK_IMPORTED_MODULE_10__["default"].info('Sent SDP');
      };
      this.connection.addSdp(sdp, sdpHandler).then(() => {
      }).catch(error => {
        _logger_js__WEBPACK_IMPORTED_MODULE_10__["default"].error('Error adding SDP', error);
      });
    }
  }
}


/***/ }),

/***/ "./src/peer/peers-panel.js":
/*!*********************************!*\
  !*** ./src/peer/peers-panel.js ***!
  \*********************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return PeersPanel; });
/* harmony import */ var _logger_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../logger.js */ "./src/logger.js");
/*
 * Copyright (c) 2020 Peter Christensen. All Rights Reserved.
 * CC BY-NC-ND 4.0.
 */


class PeersPanel {

  constructor() {
    this.panel = this._panel();
    this.info = this.panel;
    this.statusMsg = this._statusMsg();
    this.setOffline();
    this.panel.append(this.statusMsg);
    this.peers = {};
    this.onOffer = () => {};
    this.getDisplayName = () => {return 'N/A'};
  }

  _panel() {
    const div = document.createElement('div');
    div.style.marginLeft = 'auto';
    div.style.marginRight = 'auto';
    div.style.maxWidth = '600px'
    div.style.padding = '1em';
    const mm = matchMedia('(min-width: 480px)');
    mm.addListener((mm) => {
      if (mm.matches) {
        div.style.maxWidth = '480px'
      } else {
        div.style.maxWidth = '100%';
      }
      for (const clientId in this.peers) {
        this._setPeerName(this.peers[clientId]);
      }
    });
    return div;
  }

  _setPeerName(peer) {
    if (peer.peerName) {
      peer.label.textContent = this.getDisplayName(peer.peerName, 480);
      peer.label.setAttribute('title', `${peer.peerName} (${peer.peerId})`);
      peer.offerButton.setAttribute(
        'title', `Connect to ${peer.peerName} (${peer.peerId})`
      );
    } else {
      peer.label.textContent = peer.peerId;
      peer.label.removeAttribute('title');
      peer.offerButton.setAttribute('title', `Connect to ${peer.peerId}`);
    }
  }

  _statusMsg() {
    const p = document.createElement('p');
    p.style.textAlign = 'center';
    return p;
  }

  setOnline() {
    this.statusMsg.innerHTML = 'Online. Waiting for others to join.';
  }

  setOffline() {
    this.statusMsg.innerHTML = 'Offline.';
  }

  addPeer(clientId, peerName) {
    if (this.peers[clientId]) {
      this.peers[clientId].added = new Date();
      if (peerName !== this.peers[clientId].peerName) {
        this.peers[clientId].peerName = peerName;
        this._setPeerName(this.peers[clientId]);
      }
      return;
    }
    if (Object.keys(this.peers).length === 0) {
      this.statusMsg.remove();
    }
    const peer = document.createElement('article');
    peer.classList.add('card');
    const section = document.createElement('section');
    section.style.padding = '0.5em';
    peer.append(section);
    const label = document.createElement('label');
    label.classList.add('button', 'pseudo');
    section.append(label);
    const offerButton = document.createElement('button')
    offerButton.textContent = 'Connect';
    offerButton.style.float = 'right';
    offerButton.addEventListener('click', () => {
      this.onOffer(clientId);
    });
    section.append(offerButton);
    peer.added = new Date();
    peer.clientId = clientId;
    peer.peerId = clientId.substr(0, 5);
    peer.peerName = peerName;
    peer.offerButton = offerButton;
    peer.label = label;
    this.peers[clientId] = peer;
    this._setPeerName(peer);
    this.panel.append(peer);
    _logger_js__WEBPACK_IMPORTED_MODULE_0__["default"].info('Added peer', clientId);
  }

  removePeer(clientId) {
    const peer = this.peers[clientId];
    delete this.peers[clientId];
    if (peer) {
      peer.remove();
      _logger_js__WEBPACK_IMPORTED_MODULE_0__["default"].info('Removed peer', clientId);
    }
    if (Object.keys(this.peers).length === 0) {
      this.panel.append(this.statusMsg);
    }
  }

  reset() {
    Object.keys(this.peers).forEach(clientId => {
      this.removePeer(clientId);
    });
  }

  clean() {
    const expired = [];
    const now = new Date();
    _logger_js__WEBPACK_IMPORTED_MODULE_0__["default"].debug('Cleaning expired peers');
    for (const clientId in this.peers) {
      const diff = now - this.peers[clientId].added;
      if (diff > 60000) {
        expired.push(clientId);
      }
    }
    for (const clientId of expired) {
      _logger_js__WEBPACK_IMPORTED_MODULE_0__["default"].info('Peer expired', clientId);
      this.removePeer(clientId);
    }
    return expired;
  }
}


/***/ }),

/***/ "./src/view.js":
/*!*********************!*\
  !*** ./src/view.js ***!
  \*********************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return View; });
/*
 *  Copyright (c) 2020 Peter Christensen. All Rights Reserved.
 *  CC BY-NC-ND 4.0.
 */
class ActivityWatcher {

  constructor(...elements) {
    this.elements = elements;
    this.activityEvents = ['mousemove', 'touchstart'];
    this.expired = 0;
    this.interval = 1000;
    this.intervalId = null;
    this.maxInactivity = 4000;
    this.isVisible = true;
  }

  _hideElements() {
    this.isVisible = false;
    this.elements.forEach((element) => {
      element.style.visibility = 'hidden';
    });
  }

  _showElements() {
    this.isVisible = true;
    this.elements.forEach((element) => {
      element.style.visibility = 'visible';
    });
  }

  _onActivity() {
    this.expired = 0;
    if (!this.isVisible) {
      this._showElements();
    }
  }

  startWatching() {
    if (!this.intervalId) {
      this.intervalId = setInterval(() => {
        this.expired += this.interval;
        if (this.isVisible && this.expired > this.maxInactivity) {
          this._hideElements();
        }
      }, this.interval);
      this.activityEvents.forEach((eventType) => {
        document.addEventListener(eventType, this._onActivity.bind(this));
      });
    }
  }

  stopWatching() {
    this.activityEvents.forEach((eventType) => {
      document.removeEventListener(eventType, this._onActivity);
    });
    clearInterval(this.intervalId);
    this.intervalId = null;
    if (!this.isVisible) {
      this._showElements();
    }
  }
}

class AlertModal {

  constructor(header) {
    this.header = header;
    this.body = this._messagePanel();
    this.footer = this._footer();
    this.modalContent = [this.header, this.body, this.footer];
    this.messageDiv = this.body.querySelector('#alert-message');
    this.message = null;
    this.onClose = () => {};
  }

  _messagePanel() {
    const section = document.createElement('section');
    const message = document.createElement('div');
    message.setAttribute('id', 'alert-message');
    message.style.textAlign = 'center';
    section.append(message);
    return section;
  }

  _footer() {
    const button = document.createElement('button');
    button.textContent = 'OK';
    button.setAttribute('title', 'Acknowledge this alert');
    button.style.float = 'right';
    button.addEventListener('click', () => {
      this.onClose();
    });
    const footer = document.createElement('footer');
    footer.append(button);
    return footer;
  }

  isActive() {
    return this.message !== null;
  }

  setMessage(message) {
    this.message = message;
    this.messageDiv.textContent = message;
  }
}

class View {

  constructor() {
    this.navBar = document.querySelector('#nav-bar');
    this.activityWatcher = new ActivityWatcher(this.navBar);
    this.navMenu = document.querySelector('#nav-menu');
    this.navStatus = document.querySelector('#nav-status');
    this.channelInfoPanel = document.querySelector('#channel-info');
    this.modalContent = document.querySelector('#modal-content');
    this.modalControl = document.querySelector('#modal-control');
    this.modalOverlay = document.querySelector('#modal-overlay');
    this.videoElement = document.querySelector('#media-player');
    this._addEscapeListener();
    this.alertModal = new AlertModal(
      this.modalHeader('Alert')
    );
    this.alertModal.onClose = this._onCloseAlert.bind(this)
    this.modal = null;
    this.oldModal = null;
  }

  _addEscapeListener() {
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') {
        if (this.modal && this.modal.onModalEscape) {
          this.modal.onModalEscape();
        } else if (this.alertModal.isActive()) {
          this._onCloseAlert();
        }
      }
    });
  }

  _setContent(container, ...elements) {
    while (container.firstChild) {
      container.firstChild.remove();
    }
    for (const element of elements) {
      container.append(element);
    }
  }

  _setModalContent(modal) {
    if (modal.enableCloseControl) {
      this.modalControl.disabled = false;
      this.modalOverlay.classList.remove('disabled');
    } else {
      this.modalControl.disabled = true;
      this.modalOverlay.classList.add('disabled');
    }
    this._setContent(this.modalContent, ...modal.modalContent);
  }

  addTrack(track) {
    if (!this.videoElement.srcObject) {
      this.videoElement.srcObject = new MediaStream();
    }
    this.videoElement.srcObject.addTrack(track);
  }

  showPlayer() {
    this.activityWatcher.startWatching();
    this.videoElement.style.display = 'unset';
    this.channelInfoPanel.style.display = 'none';
  }

  hidePlayer() {
    this.activityWatcher.stopWatching();
    if (this.videoElement.srcObject) {
      for (const track of this.videoElement.srcObject.getTracks()) {
        track.stop();
      }
      this.videoElement.srcObject = null;
    }
    this.videoElement.style.display = 'none';
    this.channelInfoPanel.style.display = 'unset';
  }

  setNavStatus(...elements) {
    this._setContent(this.navStatus, ...elements);
  }

  setNavMenu(...elements) {
    this._setContent(this.navMenu, ...elements);
  }

  setChannelInfo(...elements) {
    this._setContent(this.channelInfoPanel, ...elements);
  }

  modalHeader(title, enableCloseControl = false) {
    const heading = document.createElement('h3');
    heading.textContent = title;
    const header = document.createElement('header');
    header.append(heading);
    if (enableCloseControl) {
      const label = document.createElement('label');
      label.innerHTML = '&times;';
      label.classList.add('close');
      label.setAttribute('for', 'modal-control');
      header.append(label);
    }
    return header;
  }

  /*
   * Showing an alert message hides the existing modal, if any. The hidden
   * modal is permanently hidden and doesn't re-appear when the alert is
   * dismissed unless the hidden modal has a hasModalContent method that
   * returns something truthy.
   */

  showAlert(message) {
    this.alertModal.setMessage(message);
    this.oldModal = this.modal;
    this.modal = null;
    this._setModalContent(this.alertModal);
    this.modalControl.checked = true;
  }

  _onCloseAlert() {
    this.alertModal.message = null;
    if (this.oldModal) {
      this.modal = this.oldModal;
      this.oldModal = null;
      if (this.modal.hasModalContent && this.modal.hasModalContent()) {
        this._setModalContent(this.modal);
      } else {
        this.modal = null;
        this.modalControl.checked = false;
      }
    } else {
      this.modalControl.checked = false;
    }
  }

  /*
   * Showing a modal while the alert is active leaves the alert active and
   * replaces/sets the hidden modal, if any.
   */

  showModal(modal) {
    if (!modal || !modal.modalContent) {
      return
    }
    if (modal.hasModalContent && !modal.hasModalContent()) {
      return;
    }
    if (this.alertModal.isActive()) {
      if (modal !== this.oldModal) {
        this.oldModal = modal;
      }
    } else {
      if (modal === this.modal) {
        this.modalControl.checked = true;
      } else {
        this.modal = modal;
        this._setModalContent(modal);
        this.modalControl.checked = true;
        if (this.modal.setFocus) {
          this.modal.setFocus();
        }
      }
    }
  }

  /*
   * Hiding the modal requires a reference to the currently displayed
   * modal, or, if the alert is active, to the hidden modal. Otherwise the
   * command is ignored.
   */

  hideModal(modal) {
    if (!modal) {
      return;
    }
    if (this.alertModal.isActive()) {
      if (modal === this.oldModal) {
        this.oldModal = null;
      }
    } else {
      if (modal === this.modal) {
        this.modal = null;
        this.modalControl.checked = false;
      }
    }
  }
}


/***/ }),

/***/ "./src/websocket.js":
/*!**************************!*\
  !*** ./src/websocket.js ***!
  \**************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return MyWebSocket; });
/* harmony import */ var _logger_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./logger.js */ "./src/logger.js");
/*
 *  Copyright (c) 2020 Peter Christensen. All Rights Reserved.
 *  CC BY-NC-ND 4.0.
 */


class MyWebSocket {

  constructor() {
    this.socket = null;
    this.isConnecting = false;
    this.isHalted = false;
    this.retryCount = 0;
    this.retryBackoff = 5;
    this.retryMaxWait = 30;
    this.retryTimer = null;
    this.onConnect = () => {};
    this.onDisconnect = () => {};
    this.onMessage = () => {};
  }

  isConnected() {
    if (!this.socket || this.socket.readyState > 1) {
      return false;
    }
    return true;
  }

  _setRetryTimer() {
    let delay = this.retryCount * this.retryBackoff;
    if (delay > this.retryMaxWait) {
      delay = this.retryMaxWait;
    }
    if (delay) {
      delay += (
        // A random number between 0 and N-1.
        + Math.floor(Math.random() * (this.retryBackoff * 2 + 1))
        - this.retryBackoff // backoff * retries +/- backoff
      );
    }
    _logger_js__WEBPACK_IMPORTED_MODULE_0__["default"].info(`Waiting ${delay}s after ${this.retryCount} tries`);
    this.retryTimer = setTimeout(() => {
      this.retryCount += 1;
      this.connect();
    }, delay * 1000);
  }

  connect() {
    if (!this.isConnected() && !this.isConnecting) {
      this.isConnecting = true;
      this.isHalted = false;
      const socket = new WebSocket(
        `wss://${location.host}${location.pathname}/clients`
      );
      socket.onopen = (event) => {
        clearTimeout(this.retryTimer);
        if (this.isConnecting) {
          this.retryCount = 0;
          this.isConnecting = false;
          this.socket = socket;
          this.onConnect(event);
        }
      }
      socket.onclose = (event) => {
        this.onDisconnect(event);
        clearTimeout(this.retryTimer);
        this.isConnecting = false;
        if (!this.isHalted) {
          this._setRetryTimer();
        }
      }
      socket.onmessage = (event) => {
        this.onMessage(event);
      }
    }
  }

  disconnect() {
    this.isHalted = true;
    this.isConnecting = false;
    clearTimeout(this.retryTimer);
    this.retryCount = 0;
    if (this.isConnected()) {
      this.socket.close();
      this.socket = null;
    }
  }

  send(message) {
    this.socket.send(JSON.stringify(message));
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