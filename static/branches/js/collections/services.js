var app = app || {};

app.ServiceList = Backbone.Collection.extend({
	model: app.Service,
	url: '/api/v1/services/',
});

app.serviceList = new app.ServiceList();