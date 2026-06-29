"use strict";

/**
 * @typedef {Object} SMNBodyJSON
 * @property {string} [topic_urn]
 * @property {string} [timestamp]
 * @property {Object | null} [message_attributes]
 * @property {string} [message]
 * @property {string} [type]
 * @property {string} [message_id]
 * @property {string} [subject]
 */

/**
 * @typedef {Object} SMNRecordJSON
 * @property {string} [event_subscription_urn]
 * @property {string} [event_source]
 * @property {SMNBodyJSON} [smn]
 */

/**
 * @typedef {Object} SMNEventJSON
 * @property {SMNRecordJSON[]} [record]
 * @property {string} [functionname]
 * @property {string} [requestId]
 * @property {string} [timestamp]
 */

/**
 * SMN Event Class
 * Represents a Simple Message Notification event for FunctionGraph
 */
class SMNEvent {
  /**
   * @param {SMNEventJSON} event
   */
  constructor(event) {
    this._event = event || {};

    this._records = [];
    for (const record of this._event.record || []) {
      this._records.push(new SMNRecord(record));
    }
  }

  /**
   * Returns the event records.
   * @returns {SMNRecord[]} Array of event records
   */
  getRecords() {
    return this._records;
  }

  /**
   * Returns the function name.
   * @returns {string} Function name
   */
  getFunctionName() {
    return this._event.functionname || "";
  }

  /**
   * Returns the request ID.
   * @returns {string} Request ID
   */
  getRequestId() {
    return this._event.requestId || "";
  }

  /**
   * Returns the timestamp.
   * @returns {string} Event timestamp
   */
  getTimestamp() {
    return this._event.timestamp || "";
  }

  /**
   * Converts the wrapped payload back to a plain JSON object.
   * @returns {SMNEventJSON} Payload as JSON object
   */
  toJSON() {
    return this._event;
  }

}

class SMNRecord {
  /**
   * @param {SMNRecordJSON} record
   */
  constructor(record) {
    this._record = record || {};
  }

  /**
   * Returns the event subscription URN.
   * @returns {string} Event subscription URN
   */
  getEventSubscriptionUrn() {
    return this._record.event_subscription_urn || "";
  }

  /**
   * Returns the event source.
   * @returns {string} Event source
   */
  getEventSource() {
    return this._record.event_source || "";
  }

  /**
   * Returns the SMN details from the record.
   * @returns {SMNBody} SMN details object
   */
  getSMNBody() {
    return new SMNBody(this._record.smn);
  }

  /**
   * Converts the wrapped payload back to a plain JSON object.
   * @returns {SMNRecordJSON} Payload as JSON object
   */
  toJSON() {
    return this._record;
  }
}

class SMNBody {
  /**
   * @param {SMNBodyJSON} smn
   */
  constructor(smn) {
    this._smn = smn || {};
  }

  /**
   * Returns the SMN topic URN.
   * @returns {string} Topic URN
   */
  getTopicUrn() {
    return this._smn.topic_urn || "";
  }

  /**
   * Returns the SMN timestamp.
   * @returns {string} SMN timestamp
   */
  getTimestamp() {
    return this._smn.timestamp || "";
  }

  /**
   * Returns the SMN message attributes.
   * @returns {Object|null} Message attributes
   */
  getMessageAttributes() {
    return this._smn.message_attributes;
  }

  /**
   * Returns the SMN message content.
   * @returns {string} Message content
   */
  getMessage() {
    return this._smn.message || "";
  }

  /**
   * Returns the SMN type.
   * @returns {string} SMN type
   */
  getType() {
    return this._smn.type || "";
  }

  /**
   * Returns the SMN message ID.
   * @returns {string} Message ID
   */
  getMessageId() {
    return this._smn.message_id || "";
  }

  /**
   * Returns the SMN message subject.
   * @returns {string} Message subject
   */
  getSubject() {
    return this._smn.subject || "";
  }

  /**
   * Converts the wrapped payload back to a plain JSON object.
   * @returns {SMNBodyJSON} Payload as JSON object
   */
  toJSON() {
    return this._smn;
  }
}

module.exports = { SMNEvent, SMNRecord, SMNBody };
