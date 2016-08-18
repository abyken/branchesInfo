var app = app || {};

app.BranchView = Backbone.View.extend({
	className: "rTableRow",
	template: $('#branch-template').text(),
	render: function() {
		var src = this.template;
		dust.helpers.isDayChecked = function(chunk, context, bodies, params) {
			var day = params.day,
				days = context.stack.head.days;

			if(days.indexOf(day) !== -1){
				chunk.render(bodies.block, context);
				return chunk;
			}

			return chunk;
		};

		dust.helpers.getModelId = function(chunk, context, bodies, params) {
			chunk.write(this.model.get('id'));
			chunk.render(bodies.block, context);
			return chunk;
		}.bind(this);

		var compiled = dust.compile(src, 'branch-template');
		dust.loadSource(compiled);
		var context = this.model.toJSON();
		context['currency_list'] = app.currencyList.map(function(currency) {
			var currencyJson = currency.toJSON();
			if(!this.model.get('currencies'))
				return currencyJson;
			if(this.model.get('currencies').indexOf(currency.id) !== -1 || 
				this.model.get('currencies').indexOf(currency.id+"") !== -1){
				currencyJson.selected = true;
			}
			return currencyJson;
		}.bind(this));

		context['service_list'] = app.serviceList.map(function(service) {
			var serviceJson = service.toJSON();
			if(!this.model.get('services'))
				return serviceJson;
			if(this.model.get('services').indexOf(service.id) !== -1 ||
				this.model.get('services').indexOf(service.id+"") !== -1){
				serviceJson.selected = true;
			}
			return serviceJson;
		}.bind(this));

		dust.render('branch-template', context, function(err, out) {
		      this.$el.html(out);
		}.bind(this));
		return this
	},

	initialize: function() {
		this.model.on('change', this.render, this);
	},
	events: {
		'mouseup': 'closeAll',
		'dblclick .field': 'edit',
		'dblclick .schedule': 'editSchedule',
		'dblclick .break': 'editBreak',
		'dblclick .currencies': 'editCurrecies',
		'dblclick .services': 'editServices',
		'keypress .edit': 'updateBranch',
		'blur .edit': 'close',
		'click .fieldCheckBox': 'onChecked',
		'click .destroy': 'destroy',
		'click .save': 'save',
		'change .model_field': 'onModelFieldSelected',
		'change .manytomany': 'onManyToManySelected',
		'click .schedulecb': 'onScheduleChecked',
		'click .scheduletm': 'onScheduleTimeChanged',
		'click .breakcb': 'onBranchBreakChecked',
		'change .breaktm': 'onBreakTimeChanged',
	},

	edit: function(event) {
		if($(event.target).prop("tagName") === "DIV"){
			$(event.target).addClass("editing");
			this.input = $(event.target).find('input');
		}
		else {
			var parent = $(event.target).parent();
			parent.addClass("editing");
			this.input = $(event.target).next('input');
		}
		this.input.focus().val(this.input.val());
	},

	editSchedule: function(event) {
		if($(event.target).prop("tagName") === "DIV"){
			this.schedule = $(event.target).find("#schedule");
			this.label = $(event.target).find("#schedule_label");
		}
		else {
			var parent = $(event.target).parent();
			this.schedule = parent.find("#schedule");
			this.label = $(event.target);
		}
		this.label.hide();
		this.schedule.show();

	},

	editBreak: function(event) {
		if($(event.target).prop("tagName") === "DIV"){
			this.branchBreak = $(event.target).find("#break");
			this.break_label = $(event.target).find("#break_label");
		}
		else {
			var parent = $(event.target).parent();
			this.branchBreak = parent.find("#break");
			this.break_label = $(event.target);
		}
		this.break_label.hide();
		this.branchBreak.show();

	},

	editCurrecies: function(event) {
		if($(event.target).prop("tagName") === "DIV"){
			this.currencies = $(event.target).find("#currencies");
			this.currencies_label = $(event.target).find("#currencies_label");
		}
		else {
			var parent = $(event.target).parent();
			this.currencies = parent.find("#currencies");
			this.currencies_label = $(event.target);
		}
		this.currencies_label.hide();
		this.currencies.show();

	},

	editServices: function(event) {
		if($(event.target).prop("tagName") === "DIV"){
			this.services = $(event.target).find("#services");
			this.services_label = $(event.target).find("#services_label");
		}
		else {
			var parent = $(event.target).parent();
			this.services = parent.find("#services");
			this.services_label = $(event.target);
		}
		this.services_label.hide();
		this.services.show();

	},

	onScheduleChecked: function(event) {
		var name = event.target.name,
			days = [];

		$("input[name='"+name+"']:checked").each(function(index, item) {
			days.push(item.value);
		});

		this.model.setSchedule(name.substring(0, 2), "days", days);
		this.setRowEdited(true);
	},

	onScheduleTimeChanged: function(event) {
		var schedule_type = event.target.name.substring(0, 2);
			name = event.target.name.substring(3),
			value = event.target.value;

		this.model.setSchedule(schedule_type, name, value);
	},

	onBranchBreakChecked: function(event) {
		var branchBreak = this.model.get('branchBreak');
		branchBreak[event.target.name] = event.target.checked;
		this.model.update({'branchBreak': branchBreak});
		this.setRowEdited(true);
	},

	onBreakTimeChanged: function(event) {
		var branchBreak = this.model.get('branchBreak');
		branchBreak[event.target.name] = event.target.value;
		this.model.update({'branchBreak': branchBreak});
		this.setRowEdited(true);
	},

	onChecked: function(event) {
		var data = {};
		data[event.target.name] = !this.model.get(event.target.name);
		this.model.update(data);
		this.setRowEdited(true);
	},

	onModelFieldSelected: function(event) {
		var data = {};
		data[event.target.name] = $(event.target).find(":selected").val();
		this.model.update(data);
		this.setRowEdited(true);
	},

	onManyToManySelected: function(event){
		var name = event.target.name.split("__")[0],
			data = {};
			data[name] = [];
		$("input[name='"+event.target.name+"']:checked").each(function(index, item) {
			data[name].push(item.value);
		});

		this.model.update(data);
		this.setRowEdited(true);
	},

	updateBranch: function(event) {
		if(event.which == 13){
	      this.close();
	    }
	},

	close: function() {
		var value = this.input.val().trim();
		var input_name = this.input.attr("name");
		var parent = $(this.input).parent();
	    parent.removeClass('editing');
	    var data = {};
	    data[input_name] = value;
	    this.model.update(data);
	    this.setRowEdited(true);
	},

	closeSchedule: function() {
		this.schedule.hide();
		this.label.show();
	    this.setRowEdited(true);
	},

	closeBreak: function() {
		this.branchBreak.hide();
		this.break_label.show();
	    this.setRowEdited(true);
	},

	closeCurrencies: function() {
		this.currencies.hide();
		this.currencies_label.show();
	    this.setRowEdited(true);
	},

	closeServices: function() {
		this.services.hide();
		this.services_label.show();
	    this.setRowEdited(true);
	},

	closeAll: function(event) {
		if(this.schedule && this.label)
			if(!this.schedule.parent().is(event.target) && this.schedule.parent().has(event.target).length === 0){
				this.closeSchedule();
			}

		if(this.branchBreak && this.break_label)
			if(!this.branchBreak.parent().is(event.target) && this.branchBreak.parent().has(event.target).length === 0){
				this.closeBreak();
			}

		if(this.currencies && this.currencies_label)
			if(!this.currencies.parent().is(event.target) && this.currencies.parent().has(event.target).length === 0){
				this.closeCurrencies();
			}

		if(this.services && this.services_label)
			if(!this.services.parent().is(event.target) && this.services.parent().has(event.target).length === 0){
				this.closeServices();
			}
				
		if(this.input)
			if (!this.input.parent().is(event.target) && this.input.parent().has(event.target).length === 0) 
				this.close();
	},

	destroy: function(event) {
		this.model.destroy({
								success: function(model) { 
										app.branchList.resetIndexes(); 
										this.remove() 
									}.bind(this), 
								error: function(err) { console.log("err", err) }.bind(this) 
							});
	},

	save: function() {
		this.model.set("isEdited", undefined);
		this.model.save(this.model, {error: function(){ this.model.set("isEdited", true) }.bind(this), success: function()  {this.setRowEdited(false) }.bind(this) });
	},

	setRowEdited: function(isEdited) {
		if(!this.$el.hasClass("rowEdited") && isEdited)
	    	this.$el.addClass("rowEdited");
	    else if(this.$el.hasClass("rowEdited") && !isEdited)
	    	this.$el.removeClass("rowEdited");
	}
})