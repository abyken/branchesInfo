var app = app || {};

app.AppView = Backbone.View.extend({
	el: '#app',
	initialize: function() {
		app.branchList.on('add', this.addAll, this);
		app.branchList.on('reset', this.addAll, this);
		app.branchList.fetch({success: this.hideSpinner});
		this.addSearchBar();
		$(window).scroll(this.fetchByPage.bind(this));
	},
	events: {
		'click #add-row': 'initializeRow',
		'click #load_more': 'fetchNext',
	},
	initializeRow: function() {
		this.showSpinner();
		$('#branch-list').html('');
		app.branchList.create(this.getBranchDefaultAttributes());
	},
	addOne: function(branchItem) {
		var view = new app.BranchView({model: branchItem});
		if(branchItem.isNew())
			$('#branch-list').prepend(view.render().el);
		else
			$('#branch-list').append(view.render().el);
		$('#spinner').hide();
	},
	addAll: function() {
		app.branchList.each(this.addOne, this);
		this.showLoadMore();
	},
	addSearchBar: function() {
		this.$('#search-bar').html('');
		var search = new app.Search({
										type: "-1"
									});
		var view = new app.SearchView({model: search});
		$('#search-bar').append(view.render().el);
	},
	getBranchDefaultAttributes: function() {
		return {}
	},

	fetchByPage: function(event) {
		this.hideLoadMore();
		if($(window).scrollTop() + $(window).innerHeight() >= window.document.documentElement.scrollHeight) {
			if(app.branchList.next){
				this.showSpinner();
            	app.branchList.fetch({url: app.branchList.next, remove: false, success: this.hideSpinner});
			}
        }
	},

	fetchNext: function() {
		if(app.branchList.next){
			this.showSpinner();
        	app.branchList.fetch({url: app.branchList.next, remove: false, success: this.hideSpinner});
		}
	},

	hideSpinner: function() {
		$('#spinner').hide();
	},

	showSpinner: function() {
		$('#spinner').show();
	},

	hideLoadMore: function() {
		$('#load_more').hide();
	},

	showLoadMore: function() {
		if(app.branchList.total > 15)
			$('#load_more').show();
	}

});