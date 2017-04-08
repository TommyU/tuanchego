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
INT_STRNIG={
	"type":"string",
	"pattern":"^(\d)+$"
}

get_brand_acts_schema={
	"type":"object",
	"properties":{
		"brand_id":UINT32,
		"lid":UINT32,
		'page_index':UINT32,
		'page_size':UINT32
	},
	"required":["lid"]
}

get_car_acts_schema={
	"type":"object",
	"properties":{
		"lid":INT_STRNIG,
		"brand_id":INT_STRNIG,
		"price":{
			"type":"string",
			"pattern": "^[0-5]{1,1}$"
		},
		"size":{
			"type":"string",
			"pattern": "^[0-8]{1,1}$"
		}
	},
	"required":["lid"],
}

join_acts_by_brand_schema={
	"type":"object",
	"properties":{
			'aid':UINT32,
			#----step 1-------
			'name':NULLABLE_STRING,
			'phone':STRING,
			'way':{
				"type":"string",
				"pattern":"^([0-3]){1,1}$",
			},#
			#----step 2-------
			'loc':{
				"type":"object",
				"properties":{
					'province':STRING,#省,
					'city':STRING,#市，
					'district':NULLABLE_STRING,#区域，
					'street':NULLABLE_STRING,#街道
				}
			},
			'car_id':UINT32,#意向车
			'version':NULLABLE_STRING,#意向车款,
			'color':{
				"type":"string",
				"pattern":"^([0-6]){1,1}$",
			},#车款颜色,
			'when':{
				"type":"string",
				"pattern":"^([0-4]){1,1}$",
			},#购车时间(一周内 半个月内 一个月内 三个月内 不确定),
			'check_way':{
				"type":"string",
				"pattern":"^([0-2]){1,1}$",
			},#看车途径（网络 4S店 其他），
			'fenqi':{
				"type":"number",
				"pattern":"^(0|1){1,1}$",
			},#是否分期（是 否）,
			'known_cut':UINT32,#已知优惠（xx元/不确定-0）	
	},
	"required":["aid", "phone"]
}

join_acts_by_car_schema={
	"type":"object",
	"properties":{
		'aid':UINT32,
		'name':NULLABLE_STRING,
		'phone':{
			"type":"string",
			"pattern":"^(\d){11,11}$"
		},
		'way':{
			"type":"string",
			"pattern":"^([0-3]){1,1}$",
		}
	},
	"required":["aid", "phone"]
}