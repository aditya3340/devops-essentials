resource "kubernetes_namespace" "argocd" {
  metadata {
    name = "argocd"
  }
}

resource "helm_release" "argo" {

  depends_on       = [kubernetes_namespace.argocd]
  name             = "argocd"
  repository       = "https://argoproj.github.io/argo-helm"
  chart            = "argo-cd"
  namespace        = kubernetes_namespace.argocd.metadata[0].name
  create_namespace = false

  values = [file("${path.module}/argocd/values-${terraform.workspace}.yaml")]

}   