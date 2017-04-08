from .models import Brand

def gen_rel():
	html=''
	for brand in Brand.objects.all():
		html+="""<span ng-click="vm.change_brand(%d)" ng-hide="vm.brand_initial!='%s'"><a rel="%s" data-hot="" ng-class="vm.brand_classes[%d]" href="javascript:void(0);">%s</a></span>\n"""%(
				brand.id,
				brand.initial,
				brand.initial,
				brand.id,
				brand.name
			)
	with open('/tmp/rels', 'w') as f:
		f.write(html)

	return html;

if __name__=='__main__':
	print gen_rel()