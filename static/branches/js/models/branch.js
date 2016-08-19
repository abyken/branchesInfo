var app = app || {};

app.Branch = Backbone.Model.extend({
	url: function() {
		var base = "/api/v1/branches/";
		if(this.isNew()) return base;

		return base + this.id + "/";
	},

	original: null, 
	
	update: function(data, isEditedCallback) {
		if(!this.original)
			this.original = this.clone();

		for(var key in data){
			switch(key) {
				case "currencies":
					this.set('currencies_verbose', app.branchList.getCurrenciesVerbose(data[key]));
					break;
				case "services":
					this.set('services_verbose', app.branchList.getServicesVerbose(data[key]));
					break;
				case "branchBreak":
					this.set('break_verbose', app.branchList.getBreakVerbose(data[key]));
					break;
				case "schedule":
					this.set('schedule_verbose', app.branchList.getScheduleVerbose(data[key], this.get('isAroundTheClock')));
					break;
				case "isAroundTheClock":
					this.set('schedule_verbose', app.branchList.getScheduleVerbose(this.get('schedule'), data[key]));
					break;

				default:
					break;
			}
			this.set(key, data[key]);
		}
		var isEdited = false;
		if(this.original){
			for(var key in this.original.attributes) {
				if(this.original.get(key) !== this.get(key)) {
					isEdited = true;
					break;
				}

			}
		}
		isEditedCallback(isEdited);
	},

	setSchedule: function(schedule_type, name, value, isEditedCallback) {
		var schedule_data = this.schedule_type(schedule_type),
			schedule_item = schedule_data.schedule[schedule_data.index];

		schedule_item[name] = value;

		this.update({schedule: schedule_data.schedule}, isEditedCallback);
	},

	schedule_type: function(schedule_type) {
		var data = {
						schedule: this.get('schedule')
					};
		data.schedule.forEach(function(item, index) {
			if(item.type === schedule_type){
				data['index'] = index;				
			}
		});

		return data;
	}
});