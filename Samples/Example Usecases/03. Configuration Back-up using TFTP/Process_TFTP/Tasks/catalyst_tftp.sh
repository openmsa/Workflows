#!/bin/bash

TARGET_CATALYST=$1
CATALYST_USER=$2
CATALYST_PASS=$3
CATALYST_ENABLE=$4
TFTP_PATH=$5

expect << HEREDOCUMENT_EOF
set timeout 10
spawn telnet $TARGET_CATALYST
expect "Username: "
send -- "$CATALYST_USER\n"
expect "Password: "
send -- "$CATALYST_PASS\n"
expect {
  "Login invalid" { exit 2 }
  ">"
}
send -- "terminal length 0\n"
expect ">"
send -- "enable\n"
expect "Password: "
send -- "$CATALYST_ENABLE\n"
expect {
  "Password: " { exit 3 }
  "Bad secrets" { exit 3 }
  "#"
}
send -- "copy running-config $TFTP_PATH\n"
send -- "\n"
send -- "\n"
send -- "\n"
set timeout 60
expect {
  "Error opening" { exit 4 }
  "#"
}
send -- "write memory\n"
send -- "exit\n"
expect eof
HEREDOCUMENT_EOF

exit $?
