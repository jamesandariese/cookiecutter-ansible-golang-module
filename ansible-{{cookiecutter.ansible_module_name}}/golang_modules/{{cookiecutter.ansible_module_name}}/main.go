package main

import "encoding/json"
import "os"
import "math/big"
import "log"
import "crypto/rand"
import "strings"

type AnsibleInput struct {
  AnsibleCheckMode bool `json:"_ansible_check_mode"`
  AnsibleNoLog bool `json:"_ansible_no_log"`
  AnsibleDebug bool `json:"_ansible_debug"`
  AnsibleDiff bool `json:"_ansible_diff"`
  AnsibleKeepRemoteFiles bool `json:"_ansible_keep_remote_files"`
  AnsibleVerbosity int `json:"_ansible_verbosity"`
  AnsibleSocket string `json:"_ansible_socket"`
  AnsibleShellExecutable string `json:"_ansible_shell_executable"`
  AnsibleTmpdir string `json:"_ansible_tmpdir"`
  AnsibleRemoteTmp string `json:"_ansible_remote_tmp"`
  AnsibleVersion string `json:"_ansible_version"`
  AnsibleModuleName string `json:"_ansible_module_name"`
  AnsibleSyslogFacility string `json:"_ansible_syslog_facility"`
  AnsibleStringConversionAction string `json:"_ansible_string_conversion_action"`
  AnsibleSelinuxSpecialFs []string `json:"_ansible_selinux_special_fs"`
}

type PrimeInput struct {
	AnsibleInput
	Bits int `json:"bits"`
}

type AnsibleOutput struct {
	Changed bool      `json:"changed"`
	Failed  bool      `json:"failed"`
	Msg     string    `json:"msg"`
	MsgLines []string `json:"msg_lines"`
}

type PrimeAnsibleOutput struct {
	AnsibleOutput
	Prime *big.Int `json:"prime"`
}

var loggerBuffer *strings.Builder
var logger *log.Logger

func init() {
	loggerBuffer = &strings.Builder{}
	logger = log.New(loggerBuffer, "GOLANG: ", log.Ldate | log.Ltime | log.Lmicroseconds | log.Llongfile | log.Lmsgprefix)
}

func fatalAnsibleResponse(err error) {
	var output AnsibleOutput
	logger.Println("error: ", err.Error())
	output.Msg = loggerBuffer.String()
	output.Failed = true
	output.Changed = false

	b, err := json.Marshal(output)
	if err != nil {
		b = []byte(`{"msg": "module error and could not create json response", "failed": true, "changed": false}`)
	}
	os.Stdout.Write(b)
	os.Exit(0)
}


func main() {
        var input PrimeInput
	var output PrimeAnsibleOutput

	if len(os.Args) > 1 {
		f, err := os.Open(os.Args[1])
		if err != nil {
			fatalAnsibleResponse(err)
		}
		decoder := json.NewDecoder(f)
		decoder.Decode(&input)
	}

	logger.Printf("Ansible verbosity is %v", input.AnsibleVerbosity)

	bits := int(2048)
	if input.Bits > 0 {
		bits = input.Bits
	}

	prime, err := rand.Prime(rand.Reader, bits)
	if err != nil {
		fatalAnsibleResponse(err)
	}

	logger.Printf("Prime generated")
	output.Msg = loggerBuffer.String()
	output.Changed = true
	output.Prime = prime

	b, err := json.Marshal(output)
	if err != nil {
		fatalAnsibleResponse(err)
	}
	os.Stdout.Write(b)
}
