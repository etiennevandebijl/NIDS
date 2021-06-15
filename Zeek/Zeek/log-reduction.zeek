event zeek_init()
    {
    Log::disable_stream(DCE_RPC::LOG);
    Log::disable_stream(DHCP::LOG);
    Log::disable_stream(DPD::LOG);
    Log::disable_stream(Files::LOG);
    Log::disable_stream(IRC::LOG);
    Log::disable_stream(KRB::LOG);
    Log::disable_stream(mysql::LOG);
    Log::disable_stream(NTP::LOG);
    Log::disable_stream(NTLM::LOG);
    Log::disable_stream(PacketFilter::LOG);
    Log::disable_stream(PE::LOG);
    Log::disable_stream(RADIUS::LOG);
    Log::disable_stream(RDP::LOG);
    Log::disable_stream(RFB::LOG);
    Log::disable_stream(Reporter::LOG);
    Log::disable_stream(SIP::LOG);
    Log::disable_stream(SMB::MAPPING_LOG);
    Log::disable_stream(SMB::FILES_LOG);
    Log::disable_stream(SMTP::LOG);
    Log::disable_stream(SNMP::LOG);
    Log::disable_stream(Syslog::LOG);
    Log::disable_stream(Tunnel::LOG);
    Log::disable_stream(X509::LOG);
    Log::disable_stream(Weird::LOG);

    Log::disable_stream(DNS::LOG);
    Log::disable_stream(SSL::LOG);
#   Log::remove_default_filter(SSH::LOG);
#   Log::add_filter(SSH::LOG, [$name="ssh-filter", $exclude=set("client", "server", "direction", 
#			                                        "cipher_alg", "mac_alg", "kex_alg",
#								"host_key_alg", "host_key", "compression_alg",
#								"auth_success")]);
}

event zeek_done()
    {
    print "Done zeek!";
}

