#!/usr/bin/env python
'''
parse a MAVLink protocol XML file and generate a python implementation

Copyright Andrew Tridgell 2011
Released under GNU GPL version 3 or later
'''

import sys, textwrap, os
import mavparse, mavtemplate

t = mavtemplate.MAVTemplate()

def generate_preamble(outf, msgs, args, xml):
    print("Generating preamble")
    t.write(outf, """
'''
MAVLink protocol implementation (auto-generated by mavgen.py)

Generated from: ${FILELIST}

Note: this file has been auto-generated. DO NOT EDIT
'''

import struct, array, mavutil

class MAVLink_header(object):
    '''MAVLink message header'''
    def __init__(self, msgId, mlen=0, seq=0, srcSystem=0, srcComponent=0):
        self.mlen = mlen
        self.seq = seq
        self.srcSystem = srcSystem
        self.srcComponent = srcComponent
        self.msgId = msgId

    def pack(self):
        return struct.pack('BBBBBB', ${PROTOCOL_MARKER}, self.mlen, self.seq,
                          self.srcSystem, self.srcComponent, self.msgId)

class MAVLink_message(object):
    '''base MAVLink message class'''
    def __init__(self, msgId, name):
        self._header     = MAVLink_header(msgId)
        self._payload    = None
        self._msgbuf     = None
        self._crc        = None
        self._fieldnames = []
        self._type       = name

    def get_msgbuf(self):
        return self._msgbuf

    def get_header(self):
        return self._header

    def get_payload(self):
        return self._payload

    def get_crc(self):
        return self._crc

    def get_fieldnames(self):
        return self._fieldnames

    def get_type(self):
        return self._type

    def get_msgId(self):
        return self._header.msgId

    def get_srcSystem(self):
        return self._header.srcSystem

    def get_srcComponent(self):
        return self._header.srcComponent

    def get_seq(self):
        return self._header.seq

    def __str__(self):
        ret = '%s {' % self._type
        for a in self._fieldnames:
            v = getattr(self, a)
            ret += '%s : %s, ' % (a, v)
        ret = ret[0:-2] + '}'
        return ret            

    def pack(self, mav, payload):
        self._payload = payload
        self._header  = MAVLink_header(self._header.msgId, len(payload), mav.seq,
                                       mav.srcSystem, mav.srcComponent)
        self._msgbuf = self._header.pack() + payload
        crc = mavutil.x25crc(self._msgbuf[1:])
        if ${crc_extra}:
            crc.accumulate(chr(self.message_crcs[_header.msgId]))
        self._crc = crc.crc
        self._msgbuf += struct.pack('<H', self._crc)
        return self._msgbuf

""", {'FILELIST' : ",".join(args),
      'PROTOCOL_MARKER' : xml.protocol_marker,
      'crc_extra' : xml.crc_extra })


def generate_enums(outf, enums):
    print("Generating enums")
    outf.write("\n# enums\n")
    wrapper = textwrap.TextWrapper(initial_indent="", subsequent_indent="\t\t\t# ")
    for e in enums:
        outf.write("\n# %s\n" % e.name)
        for entry in e.entry:
            outf.write("%s = %u # %s\n" % (entry.name, entry.value, wrapper.fill(entry.description)))

def generate_message_ids(outf, msgs):
    print("Generating message IDs")
    outf.write("\n# message IDs\n")
    outf.write("MAVLINK_MSG_ID_BAD_DATA = -1\n")
    for m in msgs:
	outf.write("MAVLINK_MSG_ID_%s = %u\n" % (m.name.upper(), m.id))

def generate_classes(outf, msgs):
    print("Generating class definitions")
    wrapper = textwrap.TextWrapper(initial_indent="\t", subsequent_indent="\t")
    for m in msgs:
	outf.write("""
class MAVLink_%s_message(MAVLink_message):
	'''
%s
	'''
	def __init__(self""" % (m.name.lower(), wrapper.fill(m.description.strip())))
        if len(m.fields) != 0:
        	outf.write(", " + ", ".join(m.fieldnames))
        outf.write("):\n")
        outf.write("\t\tMAVLink_message.__init__(self, MAVLINK_MSG_ID_%s, '%s')\n" % (m.name.upper(), m.name.upper()))
        if len(m.fieldnames) != 0:
        	outf.write("\t\tself._fieldnames = ['%s']\n" % "', '".join(m.fieldnames))
        for f in m.fields:
        	outf.write("\t\tself.%s = %s\n" % (f.name, f.name))
        outf.write("""
	def pack(self, mav):
		return MAVLink_message.pack(self, mav, struct.pack('%s'""" % m.fmtstr)
        if len(m.fields) != 0:
        	outf.write(", self." + ", self.".join(m.ordered_fieldnames))
        outf.write("))\n")


def mavfmt(field):
    '''work out the struct format for a type'''
    map = {
        'float'    : 'f',
        'char'     : 'c',
        'int8_t'   : 'b',
        'uint8_t'  : 'B',
        'uint8_t_mavlink_version'  : 'B',
        'int16_t'  : 'h',
        'uint16_t' : 'H',
        'int32_t'  : 'i',
        'uint32_t' : 'I',
        'int64_t'  : 'q',
        'uint64_t' : 'Q',
        }

    if field.array_length:
        if field.type in ['char', 'int8_t', 'uint8_t']:
            return str(field.array_length)+'s'
        return str(field.array_length)+map[field.type]
    return map[field.type]

def generate_mavlink_class(outf, msgs, xml):
    print("Generating MAVLink class")

    outf.write("\n\nmavlink_map = {\n");
    for m in msgs:
        outf.write("\tMAVLINK_MSG_ID_%s : ( '%s', MAVLink_%s_message, %s, %u ),\n" % (
            m.name.upper(), m.fmtstr, m.name.lower(), m.order_map, m.crc_extra))
    outf.write("}\n\n")
    
    t.write(outf, """
class MAVError(Exception):
	'''MAVLink error class'''
	def __init__(self, msg):
            Exception.__init__(self, msg)

class MAVString(str):
	'''NUL terminated string'''
	def __init__(self, s):
		str.__init__(self)
	def __str__(self):
            i = self.find(chr(0))
            if i == -1:
                return self[:]
            return self[0:i]

class MAVLink_bad_data(MAVLink_message):
	'''
        a piece of bad data in a mavlink stream
	'''
	def __init__(self, data, reason):
		MAVLink_message.__init__(self, MAVLINK_MSG_ID_BAD_DATA, 'BAD_DATA')
		self._fieldnames = ['data', 'reason']
		self.data = data
                self.reason = reason
                self._msgbuf = data
            
class MAVLink(object):
	'''MAVLink protocol handling class'''
	def __init__(self, file, srcSystem=0, srcComponent=0):
		self.seq = 0
		self.file = file
		self.srcSystem = srcSystem
		self.srcComponent = srcComponent
                self.callback = None
                self.callback_args = None
                self.callback_kwargs = None
                self.buf = ""
                self.expected_length = 6
                self.have_prefix_error = False
                self.robust_parsing = False
                self.protocol_marker = ${protocol_marker}
                self.little_endian = ${little_endian}
                self.crc_extra = ${crc_extra}
                self.sort_fields = ${sort_fields}

        def set_callback(self, callback, *args, **kwargs):
            self.callback = callback
            self.callback_args = args
            self.callback_kwargs = kwargs
            
	def send(self, mavmsg):
		'''send a MAVLink message'''
		buf = mavmsg.pack(self)
		self.file.write(buf)
		self.seq = (self.seq + 1) % 255

        def bytes_needed(self):
            '''return number of bytes needed for next parsing stage'''
            ret = self.expected_length - len(self.buf)
            if ret <= 0:
                return 1
            return ret

        def parse_char(self, c):
            '''input some data bytes, possibly returning a new message'''
            self.buf += c
            if len(self.buf) >= 1 and ord(self.buf[0]) != ${protocol_marker}:
                magic = self.buf[0]
                self.buf = self.buf[1:]
                if self.robust_parsing:
                    m = MAVLink_bad_data(magic, "Bad prefix")
                    if self.callback:
                        self.callback(m, *self.callback_args, **self.callback_kwargs)
                    self.expected_length = 6
                    return m
                if self.have_prefix_error:
                    return None
                self.have_prefix_error = True
                raise MAVError("invalid MAVLink prefix '%s'" % magic) 
            self.have_prefix_error = False
            if len(self.buf) >= 2:
                (magic, self.expected_length) = struct.unpack('cB', self.buf[0:2])
                self.expected_length += 8
            if self.expected_length >= 8 and len(self.buf) >= self.expected_length:
                mbuf = self.buf[0:self.expected_length]
                self.buf = self.buf[self.expected_length:]
                self.expected_length = 6
                if self.robust_parsing:
                    try:
                        m = self.decode(mbuf)
                    except MAVError, reason:
                        m = MAVLink_bad_data(mbuf, reason)
                else:
                    m = self.decode(mbuf)
                if self.callback:
                    self.callback(m, *self.callback_args, **self.callback_kwargs)
                return m
            return None

	def decode(self, msgbuf):
		'''decode a buffer as a MAVLink message'''
                # decode the header
                try:
                    magic, mlen, seq, srcSystem, srcComponent, msgId = struct.unpack('cBBBBB', msgbuf[:6])
                except struct.error, emsg:
                    raise MAVError('Unable to unpack MAVLink header: %s' % emsg)
                if ord(magic) != ${protocol_marker}:
                    raise MAVError("invalid MAVLink prefix '%s'" % magic)
                if mlen != len(msgbuf)-8:
                    raise MAVError('invalid MAVLink message length. Got %u expected %u, msgId=%u' % (len(msgbuf)-8, mlen, msgId))

                if not msgId in mavlink_map:
                    raise MAVError('unknown MAVLink message ID %u' % msgId)

                # decode the payload
                (fmt, type, order_map, crc_extra) = mavlink_map[msgId]

                # decode the checksum
                try:
                    crc, = struct.unpack('<H', msgbuf[-2:])
                except struct.error, emsg:
                    raise MAVError('Unable to unpack MAVLink CRC: %s' % emsg)
                crc2 = mavutil.x25crc(msgbuf[1:-2])
                if ${crc_extra}:
                    crc2.accumulate(chr(crc_extra))
                if crc != crc2.crc:
                    raise MAVError('invalid MAVLink CRC in msgID %u 0x%04x should be 0x%04x' % (msgId, crc, crc2.crc))

                try:
                    t = struct.unpack(fmt, msgbuf[6:-2])
                except struct.error, emsg:
                    raise MAVError('Unable to unpack MAVLink payload type=%s fmt=%s payloadLength=%u: %s' % (
                        type, fmt, len(msgbuf[6:-2]), emsg))

                # terminate any strings
                tlist = list(t)
                for i in range(0, len(tlist)):
                    if isinstance(tlist[i], str):
                        tlist[i] = MAVString(tlist[i])
                t = tuple(tlist)
                # construct the message object
                try:
                    m = type(*t)
                except Exception, emsg:
                    print tlist
                    raise MAVError('Unable to instantiate MAVLink message of type %s : %s' % (type, emsg))
                m._msgbuf = msgbuf
                m._payload = msgbuf[6:-2]
                m._crc = crc
                m._header = MAVLink_header(msgId, mlen, seq, srcSystem, srcComponent)
                return m
""", xml)

def generate_methods(outf, msgs):
    print("Generating methods")

    def field_descriptions(fields):
        ret = ""
        for f in fields:
            ret += "\t\t%-18s\t: %s (%s)\n" % (f.name, f.description.strip(), f.type)
        return ret

    wrapper = textwrap.TextWrapper(initial_indent="", subsequent_indent="\t\t")

    for m in msgs:
        comment = "%s\n\n%s" % (wrapper.fill(m.description.strip()), field_descriptions(m.fields))

        sub = {'NAMELOWER'      : m.name.lower(),
               'SELFFIELDNAMES' : ", ".join(["self"]+m.fieldnames),
               'COMMENT'        : comment,
               'FIELDNAMES'     : ", ".join(m.fieldnames)}

	t.write(outf, """
	def ${NAMELOWER}_encode(${SELFFIELDNAMES}):
		'''
		${COMMENT}
		'''
		msg = MAVLink_${NAMELOWER}_message(${FIELDNAMES})
		msg.pack(self)
                return msg
            
""", sub)

	t.write(outf, """
	def ${NAMELOWER}_send(${SELFFIELDNAMES}):
		'''
		${COMMENT}
		'''
		return self.send(self.${NAMELOWER}_encode(${FIELDNAMES}))
            
""", sub)


def generate(basename, xml):
    '''generate complete python implemenation'''
    filename = basename + '.py'

    msgs = []
    enums = []
    filelist = []
    for x in xml:
        msgs.extend(x.message)
        enums.extend(x.enum)
        filelist.append(os.path.basename(x.filename))

    for m in msgs:
        if xml[0].little_endian:
            m.fmtstr = '<'
        else:
            m.fmtstr = '>'
        for f in m.ordered_fields:
            m.fmtstr += mavfmt(f)
        m.order_map = [ 0 ] * len(m.fieldnames)
        for i in range(0, len(m.ordered_fieldnames)):
            m.order_map[i] = m.fieldnames.index(m.ordered_fieldnames[i])

    print("Generating %s" % filename)
    outf = open(filename, "w")
    generate_preamble(outf, msgs, filelist, xml[0])
    generate_enums(outf, enums)
    generate_message_ids(outf, msgs)
    generate_classes(outf, msgs)
    generate_mavlink_class(outf, msgs, xml[0])
    generate_methods(outf, msgs)
    outf.close()
    print("Generated %s OK" % filename)
