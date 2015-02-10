(function(){var $,Node,Tree,methods;$=jQuery;Node=(function(){function Node(row,tree,settings){var parentId;this.row=row;this.tree=tree;this.settings=settings;this.id=this.row.data(this.settings.nodeIdAttr);parentId=this.row.data(this.settings.parentIdAttr);if(parentId!=null&&parentId!==""){this.parentId=parentId;}
this.treeCell=$(this.row.children(this.settings.columnElType)[this.settings.column]);this.expander=$(this.settings.expanderTemplate);this.indenter=$(this.settings.indenterTemplate);this.children=[];this.initialized=false;this.treeCell.prepend(this.indenter);}
Node.prototype.addChild=function(child){return this.children.push(child);};Node.prototype.ancestors=function(){var ancestors,node;node=this;ancestors=[];while(node=node.parentNode()){ancestors.push(node);}
return ancestors;};Node.prototype.collapse=function(){this._hideChildren();this.row.removeClass("expanded").addClass("collapsed");this.expander.attr("title",this.settings.stringExpand);if(this.initialized&&this.settings.onNodeCollapse!=null){this.settings.onNodeCollapse.apply(this);}
return this;};Node.prototype.expand=function(){if(this.initialized&&this.settings.onNodeExpand!=null){this.settings.onNodeExpand.apply(this);}
this.row.removeClass("collapsed").addClass("expanded");this._showChildren();this.expander.attr("title",this.settings.stringCollapse);return this;};Node.prototype.expanded=function(){return this.row.hasClass("expanded");};Node.prototype.hide=function(){this._hideChildren();this.row.hide();return this;};Node.prototype.isBranchNode=function(){if(this.children.length>0||this.row.data(this.settings.branchAttr)===true){return true;}else{return false;}};Node.prototype.updateBranchLeafClass=function(){this.row.removeClass('branch');this.row.removeClass('leaf');this.row.addClass(this.isBranchNode()?'branch':'leaf');};Node.prototype.level=function(){return this.ancestors().length;};Node.prototype.parentNode=function(){if(this.parentId!=null){return this.tree[this.parentId];}else{return null;}};Node.prototype.removeChild=function(child){var i=$.inArray(child,this.children);return this.children.splice(i,1)};Node.prototype.render=function(){var handler,settings=this.settings,target;if(settings.expandable===true&&this.isBranchNode()){handler=function(e){$(this).parents("table").treetable("node",$(this).parents("tr").data(settings.nodeIdAttr)).toggle();return e.preventDefault();};this.indenter.html(this.expander);target=settings.clickableNodeNames===true?this.treeCell:this.expander;target.off("click.treetable").on("click.treetable",handler);target.off("keydown.treetable").on("keydown.treetable",function(e){if(e.keyCode==13){handler.apply(this,[e]);}});}
if(settings.expandable===true&&settings.initialState==="collapsed"){this.collapse();}else{this.expand();}
this.indenter[0].style.paddingLeft=""+(this.level()*settings.indent)+"px";return this;};Node.prototype.reveal=function(){if(this.parentId!=null){this.parentNode().reveal();}
return this.expand();};Node.prototype.setParent=function(node){if(this.parentId!=null){this.tree[this.parentId].removeChild(this);}
this.parentId=node.id;this.row.data(this.settings.parentIdAttr,node.id);return node.addChild(this);};Node.prototype.show=function(){if(!this.initialized){this._initialize();}
this.row.show();if(this.expanded()){this._showChildren();}
return this;};Node.prototype.toggle=function(){if(this.expanded()){this.collapse();}else{this.expand();}
return this;};Node.prototype._hideChildren=function(){var child,_i,_len,_ref,_results;_ref=this.children;_results=[];for(_i=0,_len=_ref.length;_i<_len;_i++){child=_ref[_i];_results.push(child.hide());}
return _results;};Node.prototype._initialize=function(){this.render();if(this.settings.onNodeInitialized!=null){this.settings.onNodeInitialized.apply(this);}
return this.initialized=true;};Node.prototype._showChildren=function(){var child,_i,_len,_ref,_results;_ref=this.children;_results=[];for(_i=0,_len=_ref.length;_i<_len;_i++){child=_ref[_i];_results.push(child.show());}
return _results;};return Node;})();Tree=(function(){function Tree(table,settings){this.table=table;this.settings=settings;this.tree={};this.nodes=[];this.roots=[];}
Tree.prototype.collapseAll=function(){var node,_i,_len,_ref,_results;_ref=this.nodes;_results=[];for(_i=0,_len=_ref.length;_i<_len;_i++){node=_ref[_i];_results.push(node.collapse());}
return _results;};Tree.prototype.expandAll=function(){var node,_i,_len,_ref,_results;_ref=this.nodes;_results=[];for(_i=0,_len=_ref.length;_i<_len;_i++){node=_ref[_i];_results.push(node.expand());}
return _results;};Tree.prototype.loadRows=function(rows){var node,row,i;if(rows!=null){for(i=0;i<rows.length;i++){row=$(rows[i]);if(row.data(this.settings.nodeIdAttr)!=null){node=new Node(row,this.tree,this.settings);this.nodes.push(node);this.tree[node.id]=node;if(node.parentId!=null){this.tree[node.parentId].addChild(node);}else{this.roots.push(node);}}}}
for(i=0;i<this.nodes.length;i++){node=this.nodes[i].updateBranchLeafClass();}
return this;};Tree.prototype.move=function(node,destination){var nodeParent=node.parentNode();if(node!==destination&&destination.id!==node.parentId&&$.inArray(node,destination.ancestors())===-1){node.setParent(destination);this._moveRows(node,destination);if(node.parentNode().children.length===1){node.parentNode().render();}}
if(nodeParent){nodeParent.updateBranchLeafClass();}
if(node.parentNode()){node.parentNode().updateBranchLeafClass();}
node.updateBranchLeafClass();return this;};Tree.prototype.render=function(){var root,_i,_len,_ref;_ref=this.roots;for(_i=0,_len=_ref.length;_i<_len;_i++){root=_ref[_i];root.show();}
return this;};Tree.prototype._moveRows=function(node,destination){var child,_i,_len,_ref,_results;node.row.insertAfter(destination.row);node.render();_ref=node.children;_results=[];for(_i=0,_len=_ref.length;_i<_len;_i++){child=_ref[_i];_results.push(this._moveRows(child,node));}
return _results;};Tree.prototype.unloadBranch=function(node){var child,children,i;for(i=0;i<node.children.length;i++){child=node.children[i];this.unloadBranch(child);child.row.remove();delete this.tree[child.id];this.nodes.splice($.inArray(child,this.nodes),1);}
node.children=[];node.updateBranchLeafClass();return this;};return Tree;})();methods={init:function(options,force){var settings;settings=$.extend({branchAttr:"ttBranch",clickableNodeNames:false,column:0,columnElType:"td",expandable:false,expanderTemplate:"<a href='#'>&nbsp;</a>",indent:19,indenterTemplate:"<span class='indenter icon-collapse-down'></span>",initialState:"collapsed",nodeIdAttr:"ttId",parentIdAttr:"ttParentId",stringExpand:"Expand",stringCollapse:"Collapse",onInitialized:null,onNodeCollapse:null,onNodeExpand:null,onNodeInitialized:null},options);return this.each(function(){var el=$(this),tree;if(force||el.data("treetable")===undefined){tree=new Tree(this,settings);tree.loadRows(this.rows).render();el.addClass("treetable").data("treetable",tree);if(settings.onInitialized!=null){settings.onInitialized.apply(tree);}}
return el;});},destroy:function(){return this.each(function(){return $(this).removeData("treetable").removeClass("treetable");});},collapseAll:function(){this.data("treetable").collapseAll();return this;},collapseNode:function(id){var node=this.data("treetable").tree[id];if(node){node.collapse();}else{throw new Error("Unknown node '"+id+"'");}
return this;},expandAll:function(){this.data("treetable").expandAll();return this;},expandNode:function(id){var node=this.data("treetable").tree[id];if(node){node.expand();}else{throw new Error("Unknown node '"+id+"'");}
return this;},loadBranch:function(node,rows){var settings=this.data("treetable").settings,tree=this.data("treetable").tree;rows=$(rows);if(node==null){this.append(rows);}else if(node.children.length>0){var current=node;while(current.children.length>0){current=current.children[current.children.length-1];}
rows.insertAfter(current.row);}else{rows.insertAfter(node.row);}
this.data("treetable").loadRows(rows);rows.filter("tr").each(function(){tree[$(this).data(settings.nodeIdAttr)].show();});return this;},move:function(nodeId,destinationId){var destination,node;node=this.data("treetable").tree[nodeId];destination=this.data("treetable").tree[destinationId];this.data("treetable").move(node,destination);return this;},node:function(id){return this.data("treetable").tree[id];},reveal:function(id){var node=this.data("treetable").tree[id];if(node){node.reveal();}else{throw new Error("Unknown node '"+id+"'");}
return this;},unloadBranch:function(node){this.data("treetable").unloadBranch(node);return this;}};$.fn.treetable=function(method){if(methods[method]){return methods[method].apply(this,Array.prototype.slice.call(arguments,1));}else if(typeof method==='object'||!method){return methods.init.apply(this,arguments);}else{return $.error("Method "+method+" does not exist on jQuery.treetable");}};this.TreeTable||(this.TreeTable={});this.TreeTable.Node=Node;this.TreeTable.Tree=Tree;}).call(this);$(document).ready(function(){var vm=new ProfitAndLoss({"start":"2014-01-01","total_revenue":1301.0,"end":"2014-06-20","gross_profit":1301.0,"categories":[{"children":[{"accounts":[{"transaction_dr":0.0,"link":"/ledger/37","id":37,"transaction_cr":1001.0,"name":"Cigarette/Tobacco Sales"},{"transaction_dr":0.0,"link":"/ledger/36","id":36,"transaction_cr":100.0,"name":"Fuel Sales"},{"transaction_dr":0.0,"link":"/ledger/40","id":40,"transaction_cr":100.0,"name":"Newspaper Sales"},{"transaction_dr":0.0,"link":"/ledger/41","id":41,"transaction_cr":100.0,"name":"Non Tax Sales"}],"id":38,"name":"Sales"}],"accounts":[],"id":1,"name":"Revenue"},{"amount":0.0,"children":[{"amount":0.0,"name":"Opening Stock","id":1000},{"accounts":[],"id":41,"name":"Purchase"},{"accounts":[],"id":42,"name":"Direct Expenses"},{"amount":0.0,"name":"Sub Total","id":1001},{"amount":0.0,"name":"Closing Stock","id":1002}],"name":"Cost Of Goods Sold","id":2},{"amount":1301.0,"id":3,"name":"Gross Profit"},{"accounts":[],"id":4,"name":"Indirect Income"},{"children":[{"accounts":[],"id":44,"name":"Pay Head"}],"accounts":[],"id":5,"name":"Indirect Expenses"}]});ko.applyBindings(vm);$(".tree-table").treetable({initialState:'collapsed',clickableNodeNames:false,expandable:true});$('.dateinput').datepicker({format:'mm/dd/yyyy'});vm.expandRoot();});