var app = app || {};

app.AppView = Backbone.View.extend({
	el: '#app',
	initialize: function() {
		app.branchList.on('add', this.addAll, this);
		app.branchList.on('reset', this.addAll, this);
		app.branchList.fetch({success: this.hideSpinner});
		this.addSearchBar();
		$('#content').scroll(this.fetchByPage.bind(this));
	},
	events: {
		'click #add-row': 'initializeRow',
		'resize': 'setTableBody',
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
		this.setTableBody();
		$('#spinner').hide();
	},
	addAll: function() {
		app.branchList.each(this.addOne, this);
	},
	addSearchBar: function() {
		this.$('#search-bar').html('');
		var search = new app.Search({
										isFetchAll: true,
										isActive: true,
										type: "-1"
									});
		var view = new app.SearchView({model: search});
		$('#search-bar').append(view.render().el);
	},
	getBranchDefaultAttributes: function() {
		return {}
	},

	fetchByPage: function(event) {
		if($("#content").scrollTop() + $("#content").innerHeight() >= $("#content")[0].scrollHeight) {
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

    setTableBody: function() {
	    $("#content").height($(window).height() - ($("#header").height() + $("#search-bar").height()) + 200);
	}
});