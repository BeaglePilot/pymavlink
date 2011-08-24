// MESSAGE NAV_CONTROLLER_OUTPUT PACKING

#define MAVLINK_MSG_ID_NAV_CONTROLLER_OUTPUT 62

typedef struct __mavlink_nav_controller_output_t
{
 float nav_roll; ///< Current desired roll in degrees
 float nav_pitch; ///< Current desired pitch in degrees
 int16_t nav_bearing; ///< Current desired heading in degrees
 int16_t target_bearing; ///< Bearing to current waypoint/target in degrees
 uint16_t wp_dist; ///< Distance to active waypoint in meters
 float alt_error; ///< Current altitude error in meters
 float aspd_error; ///< Current airspeed error in meters/second
 float xtrack_error; ///< Current crosstrack error on x-y plane in meters
} mavlink_nav_controller_output_t;

/**
 * @brief Pack a nav_controller_output message
 * @param system_id ID of this system
 * @param component_id ID of this component (e.g. 200 for IMU)
 * @param msg The MAVLink message to compress the data into
 *
 * @param nav_roll Current desired roll in degrees
 * @param nav_pitch Current desired pitch in degrees
 * @param nav_bearing Current desired heading in degrees
 * @param target_bearing Bearing to current waypoint/target in degrees
 * @param wp_dist Distance to active waypoint in meters
 * @param alt_error Current altitude error in meters
 * @param aspd_error Current airspeed error in meters/second
 * @param xtrack_error Current crosstrack error on x-y plane in meters
 * @return length of the message in bytes (excluding serial stream start sign)
 */
static inline uint16_t mavlink_msg_nav_controller_output_pack(uint8_t system_id, uint8_t component_id, mavlink_message_t* msg,
						       float nav_roll, float nav_pitch, int16_t nav_bearing, int16_t target_bearing, uint16_t wp_dist, float alt_error, float aspd_error, float xtrack_error)
{
	msg->msgid = MAVLINK_MSG_ID_NAV_CONTROLLER_OUTPUT;

	put_float_by_index(nav_roll, 0,  msg->payload); // Current desired roll in degrees
	put_float_by_index(nav_pitch, 4,  msg->payload); // Current desired pitch in degrees
	put_int16_t_by_index(nav_bearing, 8,  msg->payload); // Current desired heading in degrees
	put_int16_t_by_index(target_bearing, 10,  msg->payload); // Bearing to current waypoint/target in degrees
	put_uint16_t_by_index(wp_dist, 12,  msg->payload); // Distance to active waypoint in meters
	put_float_by_index(alt_error, 14,  msg->payload); // Current altitude error in meters
	put_float_by_index(aspd_error, 18,  msg->payload); // Current airspeed error in meters/second
	put_float_by_index(xtrack_error, 22,  msg->payload); // Current crosstrack error on x-y plane in meters

	return mavlink_finalize_message(msg, system_id, component_id, 26, 100);
}

/**
 * @brief Pack a nav_controller_output message on a channel
 * @param system_id ID of this system
 * @param component_id ID of this component (e.g. 200 for IMU)
 * @param chan The MAVLink channel this message was sent over
 * @param msg The MAVLink message to compress the data into
 * @param nav_roll Current desired roll in degrees
 * @param nav_pitch Current desired pitch in degrees
 * @param nav_bearing Current desired heading in degrees
 * @param target_bearing Bearing to current waypoint/target in degrees
 * @param wp_dist Distance to active waypoint in meters
 * @param alt_error Current altitude error in meters
 * @param aspd_error Current airspeed error in meters/second
 * @param xtrack_error Current crosstrack error on x-y plane in meters
 * @return length of the message in bytes (excluding serial stream start sign)
 */
static inline uint16_t mavlink_msg_nav_controller_output_pack_chan(uint8_t system_id, uint8_t component_id, uint8_t chan,
							   mavlink_message_t* msg,
						           float nav_roll,float nav_pitch,int16_t nav_bearing,int16_t target_bearing,uint16_t wp_dist,float alt_error,float aspd_error,float xtrack_error)
{
	msg->msgid = MAVLINK_MSG_ID_NAV_CONTROLLER_OUTPUT;

	put_float_by_index(nav_roll, 0,  msg->payload); // Current desired roll in degrees
	put_float_by_index(nav_pitch, 4,  msg->payload); // Current desired pitch in degrees
	put_int16_t_by_index(nav_bearing, 8,  msg->payload); // Current desired heading in degrees
	put_int16_t_by_index(target_bearing, 10,  msg->payload); // Bearing to current waypoint/target in degrees
	put_uint16_t_by_index(wp_dist, 12,  msg->payload); // Distance to active waypoint in meters
	put_float_by_index(alt_error, 14,  msg->payload); // Current altitude error in meters
	put_float_by_index(aspd_error, 18,  msg->payload); // Current airspeed error in meters/second
	put_float_by_index(xtrack_error, 22,  msg->payload); // Current crosstrack error on x-y plane in meters

	return mavlink_finalize_message_chan(msg, system_id, component_id, chan, 26, 100);
}

#ifdef MAVLINK_USE_CONVENIENCE_FUNCTIONS

/**
 * @brief Pack a nav_controller_output message on a channel and send
 * @param chan The MAVLink channel this message was sent over
 * @param msg The MAVLink message to compress the data into
 * @param nav_roll Current desired roll in degrees
 * @param nav_pitch Current desired pitch in degrees
 * @param nav_bearing Current desired heading in degrees
 * @param target_bearing Bearing to current waypoint/target in degrees
 * @param wp_dist Distance to active waypoint in meters
 * @param alt_error Current altitude error in meters
 * @param aspd_error Current airspeed error in meters/second
 * @param xtrack_error Current crosstrack error on x-y plane in meters
 */
static inline void mavlink_msg_nav_controller_output_pack_chan_send(mavlink_channel_t chan,
							   mavlink_message_t* msg,
						           float nav_roll,float nav_pitch,int16_t nav_bearing,int16_t target_bearing,uint16_t wp_dist,float alt_error,float aspd_error,float xtrack_error)
{
	msg->msgid = MAVLINK_MSG_ID_NAV_CONTROLLER_OUTPUT;

	put_float_by_index(nav_roll, 0,  msg->payload); // Current desired roll in degrees
	put_float_by_index(nav_pitch, 4,  msg->payload); // Current desired pitch in degrees
	put_int16_t_by_index(nav_bearing, 8,  msg->payload); // Current desired heading in degrees
	put_int16_t_by_index(target_bearing, 10,  msg->payload); // Bearing to current waypoint/target in degrees
	put_uint16_t_by_index(wp_dist, 12,  msg->payload); // Distance to active waypoint in meters
	put_float_by_index(alt_error, 14,  msg->payload); // Current altitude error in meters
	put_float_by_index(aspd_error, 18,  msg->payload); // Current airspeed error in meters/second
	put_float_by_index(xtrack_error, 22,  msg->payload); // Current crosstrack error on x-y plane in meters

	mavlink_finalize_message_chan_send(msg, chan, 26, 100);
}
#endif // MAVLINK_USE_CONVENIENCE_FUNCTIONS


/**
 * @brief Encode a nav_controller_output struct into a message
 *
 * @param system_id ID of this system
 * @param component_id ID of this component (e.g. 200 for IMU)
 * @param msg The MAVLink message to compress the data into
 * @param nav_controller_output C-struct to read the message contents from
 */
static inline uint16_t mavlink_msg_nav_controller_output_encode(uint8_t system_id, uint8_t component_id, mavlink_message_t* msg, const mavlink_nav_controller_output_t* nav_controller_output)
{
	return mavlink_msg_nav_controller_output_pack(system_id, component_id, msg, nav_controller_output->nav_roll, nav_controller_output->nav_pitch, nav_controller_output->nav_bearing, nav_controller_output->target_bearing, nav_controller_output->wp_dist, nav_controller_output->alt_error, nav_controller_output->aspd_error, nav_controller_output->xtrack_error);
}

/**
 * @brief Send a nav_controller_output message
 * @param chan MAVLink channel to send the message
 *
 * @param nav_roll Current desired roll in degrees
 * @param nav_pitch Current desired pitch in degrees
 * @param nav_bearing Current desired heading in degrees
 * @param target_bearing Bearing to current waypoint/target in degrees
 * @param wp_dist Distance to active waypoint in meters
 * @param alt_error Current altitude error in meters
 * @param aspd_error Current airspeed error in meters/second
 * @param xtrack_error Current crosstrack error on x-y plane in meters
 */
#ifdef MAVLINK_USE_CONVENIENCE_FUNCTIONS

static inline void mavlink_msg_nav_controller_output_send(mavlink_channel_t chan, float nav_roll, float nav_pitch, int16_t nav_bearing, int16_t target_bearing, uint16_t wp_dist, float alt_error, float aspd_error, float xtrack_error)
{
	MAVLINK_ALIGNED_MESSAGE(msg, 26);
	mavlink_msg_nav_controller_output_pack_chan_send(chan, msg, nav_roll, nav_pitch, nav_bearing, target_bearing, wp_dist, alt_error, aspd_error, xtrack_error);
}

#endif

// MESSAGE NAV_CONTROLLER_OUTPUT UNPACKING


/**
 * @brief Get field nav_roll from nav_controller_output message
 *
 * @return Current desired roll in degrees
 */
static inline float mavlink_msg_nav_controller_output_get_nav_roll(const mavlink_message_t* msg)
{
	return MAVLINK_MSG_RETURN_float(msg,  0);
}

/**
 * @brief Get field nav_pitch from nav_controller_output message
 *
 * @return Current desired pitch in degrees
 */
static inline float mavlink_msg_nav_controller_output_get_nav_pitch(const mavlink_message_t* msg)
{
	return MAVLINK_MSG_RETURN_float(msg,  4);
}

/**
 * @brief Get field nav_bearing from nav_controller_output message
 *
 * @return Current desired heading in degrees
 */
static inline int16_t mavlink_msg_nav_controller_output_get_nav_bearing(const mavlink_message_t* msg)
{
	return MAVLINK_MSG_RETURN_int16_t(msg,  8);
}

/**
 * @brief Get field target_bearing from nav_controller_output message
 *
 * @return Bearing to current waypoint/target in degrees
 */
static inline int16_t mavlink_msg_nav_controller_output_get_target_bearing(const mavlink_message_t* msg)
{
	return MAVLINK_MSG_RETURN_int16_t(msg,  10);
}

/**
 * @brief Get field wp_dist from nav_controller_output message
 *
 * @return Distance to active waypoint in meters
 */
static inline uint16_t mavlink_msg_nav_controller_output_get_wp_dist(const mavlink_message_t* msg)
{
	return MAVLINK_MSG_RETURN_uint16_t(msg,  12);
}

/**
 * @brief Get field alt_error from nav_controller_output message
 *
 * @return Current altitude error in meters
 */
static inline float mavlink_msg_nav_controller_output_get_alt_error(const mavlink_message_t* msg)
{
	return MAVLINK_MSG_RETURN_float(msg,  14);
}

/**
 * @brief Get field aspd_error from nav_controller_output message
 *
 * @return Current airspeed error in meters/second
 */
static inline float mavlink_msg_nav_controller_output_get_aspd_error(const mavlink_message_t* msg)
{
	return MAVLINK_MSG_RETURN_float(msg,  18);
}

/**
 * @brief Get field xtrack_error from nav_controller_output message
 *
 * @return Current crosstrack error on x-y plane in meters
 */
static inline float mavlink_msg_nav_controller_output_get_xtrack_error(const mavlink_message_t* msg)
{
	return MAVLINK_MSG_RETURN_float(msg,  22);
}

/**
 * @brief Decode a nav_controller_output message into a struct
 *
 * @param msg The message to decode
 * @param nav_controller_output C-struct to decode the message contents into
 */
static inline void mavlink_msg_nav_controller_output_decode(const mavlink_message_t* msg, mavlink_nav_controller_output_t* nav_controller_output)
{
#if MAVLINK_NEED_BYTE_SWAP
	nav_controller_output->nav_roll = mavlink_msg_nav_controller_output_get_nav_roll(msg);
	nav_controller_output->nav_pitch = mavlink_msg_nav_controller_output_get_nav_pitch(msg);
	nav_controller_output->nav_bearing = mavlink_msg_nav_controller_output_get_nav_bearing(msg);
	nav_controller_output->target_bearing = mavlink_msg_nav_controller_output_get_target_bearing(msg);
	nav_controller_output->wp_dist = mavlink_msg_nav_controller_output_get_wp_dist(msg);
	nav_controller_output->alt_error = mavlink_msg_nav_controller_output_get_alt_error(msg);
	nav_controller_output->aspd_error = mavlink_msg_nav_controller_output_get_aspd_error(msg);
	nav_controller_output->xtrack_error = mavlink_msg_nav_controller_output_get_xtrack_error(msg);
#else
	memcpy(nav_controller_output, msg->payload, 26);
#endif
}
