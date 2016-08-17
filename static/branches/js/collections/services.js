var app = app || {};

app.ServiceList = Backbone.Collection.extend({
	model: app.Service,
	url: '/api/v1/services/',
	parse: function(response) {
		return response.results;
	}
});

app.serviceList = new app.ServiceList();