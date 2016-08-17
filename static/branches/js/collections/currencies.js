var app = app || {};

app.CurrencyList = Backbone.Collection.extend({
	model: app.Currency,
	url: '/api/v1/currencies/',
});

app.currencyList = new app.CurrencyList();