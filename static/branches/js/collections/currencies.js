var app = app || {};

app.CurrencyList = Backbone.Collection.extend({
	model: app.Currency,
	url: '/api/v1/currencies/',
	parse: function(response) {
		return response.results;
	}
});

app.currencyList = new app.CurrencyList();