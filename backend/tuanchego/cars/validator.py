# -*- coding:utf-8 -*-
STRING={
	"type":"string", "minLength":1
}
NULLABLE_STRING={
	"type":"string"
}
UINT32={
	"type":"number", "minimun":0, "maximum":4294967295
}

get_cars_schema={
	"type":"object",
	"properties":{
		"price":{
			"type":"string",
			"pattern": "^[0-5]{1,1}$"
		},
		"size":{
			"type":"string",
			"pattern": "^[0-8]{1,1}$"
		},
		"brand":UINT32,
		"dispatchment":{
			"type":"number",
			"pattern": "^[1-9]{1,1}$"
		},
		"gearbox":{
			"type":"string",
			"pattern": "^[0-4]{1,1}$"
		},
		"country":{
			"type":"string",
			"pattern": "^[0-7]{1,1}$"
		},
	},
	"required":[]
}

get_car_info_schema={
	"type":"object",
	"properties":{
		"bid":{
			"type":"string",
			"pattern":"^(\d)+$",
		},
		"lv":{
			"type":"string", 
			"pattern":"^(brand|car)$"
		}
	},
	"required":["lv"]
}

get_elec_cars_schema={
	"type":"object",
	"properties":{
		"lid":{
			"type":"string",
			"pattern":"^(\d)+$"
		}
	},
	"required":["lid"]
}