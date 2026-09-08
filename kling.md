调用方式：
```
curl https://agentrs.jd.com/api/saas/plugin-u/v1/exec/text2video \
	-X POST \
	-H "Content-Type: application/json" \
	-H "Authorization: Bearer $your_api_key" \
	-d '{
		"model_name": "kling-v1",
		"prompt": "画一幅图",
		"negative_prompt": "",
		"cfg_scale": 0.5,
		"mode": "std",
		"camera_control": {
			"type": "simple",
			"config": {
				"horizontal": 8,
				"vertical": 0,
				"pan": 0,
				"tilt": 0,
				"roll": 0,
				"zoom": 0
			}
		},
		"aspect_ratio": "16:9",
		"duration": "5",
		"callback_url": "",
		"external_task_id": "",
		"sound": "off"
	}'
```

keys: RsCenterCH-wos2rpj/Z+OaspXkNL8fqwUG3AxCIhdZ7gRUYOE67ss=