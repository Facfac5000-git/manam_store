from django.urls import path

from .views import (
    create_buyer,
    create_supplier,
    create_product,
    create_order,
    edit_buyer,
    edit_supplier,
    edit_product,
    delete_buyer,
    delete_supplier,
    delete_product,

    billing,
    cash_control,
    calendar,

    get_product_by_barcode,
    get_product_by_id,
    get_order_data,
    get_alert_stock_products,
    get_alert_expire_products,

    BuyerListView,
    SupplierListView,
    ProductListView,
    OrderListView,

    st_time_parallel,
    st_best_day,
    st_best_product
)

urlpatterns = [
    path('create-buyer/', create_buyer, name='create-buyer'),
    path('create-supplier/', create_supplier, name='create-supplier'),
    path('create-product/', create_product, name='create-product'),
    path('create-order/', create_order, name='create-order'),

    path('edit-buyer', edit_buyer, name='edit-buyer'),
    path('edit-supplier', edit_supplier, name='edit-supplier'),
    path('edit-product', edit_product, name='edit-product'),

    path('delete-buyer', delete_buyer, name='delete-buyer'),
    path('delete-supplier', delete_supplier, name='delete-supplier'),
    path('delete-product', delete_product, name='delete-product'),

    path('buyer-list/', BuyerListView.as_view(), name='buyer-list'),
    path('supplier-list/', SupplierListView.as_view(), name='supplier-list'),
    path('product-list/', ProductListView.as_view(), name='product-list'),
    path('order-list/', OrderListView.as_view(), name='order-list'),

    path('billing/', billing, name='billing'),
    path('cash_control/', cash_control, name='cash-control'),
    path('calendar/', calendar, name='calendar'),

    path('st_time_parallel/', st_time_parallel, name='st-time-parallel'),
    path('st_best_day/', st_best_day, name='st-best-day'),
    path('st_best_product/', st_best_product, name='st-best-product'),

    path('ajax/get_product_by_barcode/', get_product_by_barcode, name='get-product-by-barcode'),
    path('ajax/get_product_by_id/', get_product_by_id, name='get-product-by-id'),
    path('ajax/get_order_data/', get_order_data, name='get-order-data'),
    path('ajax/get_alert_stock_products/', get_alert_stock_products, name='get-alert-stock-products'),
    path('ajax/get_alert_expire_products/', get_alert_expire_products, name='get-alert-expire-products'),
]
