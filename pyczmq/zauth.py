from pyczmq._cffi import C, ffi

ffi.cdef('''
/*  =========================================================================
    zauth - authentication for ZeroMQ security mechanisms

    -------------------------------------------------------------------------
    Copyright (c) 1991-2013 iMatix Corporation <www.imatix.com>
    Copyright other contributors as noted in the AUTHORS file.

    This file is part of CZMQ, the high-level C binding for 0MQ:
    http://czmq.zeromq.org.

    This is free software; you can redistribute it and/or modify it under
    the terms of the GNU Lesser General Public License as published by the
    Free Software Foundation; either version 3 of the License, or (at your
    option) any later version.

    This software is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABIL-
    ITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General
    Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
    =========================================================================
*/

//  Opaque class structure
typedef struct _zauth_t zauth_t;

//  Constructor
//  Install authentication for the specified context. Returns a new zauth
//  object that you can use to configure authentication. Note that until you
//  add policies, all incoming NULL connections are allowed (classic ZeroMQ
//  behaviour), and all PLAIN and CURVE connections are denied. If there was
//  an error during initialization, returns NULL.
 zauth_t *
    zauth_new (zctx_t *ctx);
    
//  Allow (whitelist) a single IP address. For NULL, all clients from this
//  address will be accepted. For PLAIN and CURVE, they will be allowed to
//  continue with authentication. You can call this method multiple times 
//  to whitelist multiple IP addresses. If you whitelist a single address,
//  any non-whitelisted addresses are treated as blacklisted.
 void
    zauth_allow (zauth_t *self, char *address);

//  Deny (blacklist) a single IP address. For all security mechanisms, this
//  rejects the connection without any further authentication. Use either a
//  whitelist, or a blacklist, not not both. If you define both a whitelist 
//  and a blacklist, only the whitelist takes effect.
 void
    zauth_deny (zauth_t *self, char *address);

//  Configure PLAIN authentication for a given domain. PLAIN authentication
//  uses a plain-text password file. The filename is treated as a printf 
//  format. To cover all domains, use "*". You can modify the password file
//  at any time; it is reloaded automatically.
 void
    zauth_configure_plain (zauth_t *self, char *domain, char *filename, ...);
    
//  Configure CURVE authentication for a given domain. CURVE authentication
//  uses a directory that holds all public client certificates, i.e. their
//  public keys. The certificates must be in zcert_save () format. The 
//  location is treated as a printf format. To cover all domains, use "*". 
//  You can add and remove certificates in that directory at any time. 
//  To allow all client keys without checking, specify CURVE_ALLOW_ANY
//  for the location.
 void
    zauth_configure_curve (zauth_t *self, char *domain, char *location, ...);
    
//  Enable verbose tracing of commands and activity
 void
    zauth_set_verbose (zauth_t *self, bool verbose);
    
//  Destructor
 void
    zauth_destroy (zauth_t **self_p);

//  Selftest
 int
    zauth_test (bool verbose);
''')

def new(ctx):
    auth = C.zauth_new(ctx)
    def destroy(c):
        C.zauth_destroy(ptop('zauth_t', c))
    return ffi.gc(auth, destroy)

allow = C.zauth_allow
deny = C.zauth_deny
configure_plain = C.zauth_configure_plain
configure_curve = C.zauth_configure_curve
set_verbose = C.zauth_set_verbose
test = C.zauth_test