var app = app || {};

app.BranchList = Backbone.Collection.extend({
	model: app.Branch,
	url: '/api/v1/branches/',
	all: [],
	next: '/api/v1/branches/',
	page: 0,
	total: 0,
	parse: function(response) {
		if(this.next == response.next && this.page != 0)
			return [];

		this.page++;
		this.next = response.next;
		this.total = response.count;
		response.results.map(function(branch, index) {
			branch.index = index + 1 + (this.page - 1) * 15;
			branch.currencies_verbose = this.getCurrenciesVerbose(branch.currencies);
			branch.schedule_verbose = this.getScheduleVerbose(branch.schedule, branch.isAroundTheClock);
			branch.break_verbose = this.getBreakVerbose(branch.branchBreak);
			branch.services_verbose = this.getServicesVerbose(branch.services);
		}.bind(this));
		return response.results;
	},

	create: function(data) {
		Backbone.Collection.prototype.create.call(this, data, {
			success: function(response) {
				var model = this.at(this.length - 1);
				model.set("index", "Новая запись");
			}.bind(this)
		});
	},

	resetIndexes: function(){
		this.map(function(branch, index) {
			branch.set('index', index + 1);
		})
	},

	search: function(attributes, success) {
		this.page = 0;
		var query = "", first = true, data = {};
		if(!attributes)
			return;

		for(var key in attributes) {
			if(attributes[key] === "-1" || 
				(key === "currencies" && attributes["type"] === "branch") ||
				(key === "services" && attributes["type"] !== "branch") || 
				(key === "clients" && attributes["type"] !== "branch") || 
				(key === "isCashIn" && attributes["type"] === "branch"))
				continue;

			data[key] = attributes[key];

			if(first){
				query += "?" + key + "=" + attributes[key];
				first = false;
				continue;
			}

			query += "&" + key + "=" + attributes[key];
		}
		this.fetch({data: data, success: success});
	},

	getCurrenciesVerbose: function(ids) {
		var vals_array = ids.map(function(id) {
			return app.currencyList.get(id).get('code');
		});

		return vals_array.join(", ");
	},

	getScheduleVerbose: function(value, isAroundTheClock) {
		var days_list = ["MON","TUE","WED","THU","FRI","SAT","SUN"];
		function getIntervalString(days) {
			var days_short = {
							"MON": "пн",
							"TUE": "вт",
							"WED": "ср",
							"THU": "чт",
							"FRI": "пт",
							"SAT": "сб",
							"SUN": "вс"
						},
			day_start = "",
			day_end = "";

			if(days.length === 1)
				return days_short[days[0]]

			for(var i=0; i<7; i++){
				if(days.indexOf(days_list[i]) !== -1) {
					if(!day_start)
						day_start = days_short[days_list[i]];

					day_end = days_short[days_list[i]];
				}
			}

			return day_start + "-" + day_end;
		}

		if(isAroundTheClock)
			return 'Круглосуточно'

		var unicode_string = [], 
			string_parts = "",
			working_days = [];
		for(var i=0; i<value.length; i++){

			if(value[i].days.length === 0){
				continue;
			}
			var days_interval = getIntervalString(value[i].days);
			working_days = working_days.concat(value[i].days);

			var time = value[i].time_from + "-" + value[i].time_to;
			string_parts += days_interval + ": ";
			string_parts += time;
			unicode_string.push(string_parts);
			string_parts = "";
		}

		var days_off = _.difference(days_list, working_days)

		if(days_off){
			var days_interval = getIntervalString(days_off);
			string_parts = days_interval + ": выходной";
			unicode_string.push(string_parts);
		}
		return unicode_string.join("; ");
	},

	getBreakVerbose: function(value) {
		if(value.isWithoutBreak)
			return "Без перерыва"

		return value.time_from + "-" + value.time_to;
	},

	getServicesVerbose: function(ids) {
		var vals_array = ids.map(function(id) {
			return app.serviceList.get(id).get('name');
		});

		return vals_array.join(", ");
	},

	getCurrenciesList: function(ids) {
		var currencies_list = app.currencyList.map(function(currency) {
			var currencyJson = currency.toJSON();
			if(ids.indexOf(currency.id) !== -1){
				currencyJson.selected = true;
			}
			return currencyJson;
		});

		return currencies_list
	},

	getServicesList: function(ids) {
		var services_list = app.serviceList.map(function(service) {
			var serviceJson = service.toJSON();
			if(ids.indexOf(service.id) !== -1){
				serviceJson.selected = true;
			}
			return serviceJson;
		});

		return services_list;
	},

});

app.branchList = new app.BranchList();