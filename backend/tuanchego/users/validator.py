# -*- coding:utf-8 -*-
STRING={
	"type":"string", "minLength":1
}
UINT32={
	"type":"number", "minimun":0, "maximum":4294967295
}

login_schema={
	"type":"object",
	"properties":{
		"phone":STRING,
		"passwd":STRING
	},
	"required":["phone","passwd"]
}
reg_schema={
	"type":"object",
	"properties":{
		"phone":STRING,
		"passwd":STRING,
		"sms":STRING
	},
	"required":["phone","passwd","sms"]
}

reg_sms_schema={
	"type":"object",
	"properties":{
		"phone":
		{
			"type":"string",
			"pattern":"^(\d){11,11}$"
		},
	},
	"required":["phone"]
}