from .views import ClusterManageView

urls = {
    ClusterManageView: [r'<user_id>', r'update/<cluster_id>', r'delete/<cluster_id>']
}