# output "argocd_ui_access_command" {
#   description = "value"
#   value       = "kubectl port-forward svc/argocd-server -n argocd 8080:443"
# }

# output "argocd_initial_password" {
#   description = "value"
#   value       = "kubectl get secret argocd-inital-admin-secret -n argocd -o jsonpath='{.data.password}' | base64 -d"
# }