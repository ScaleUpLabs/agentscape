data "template_file" "k8s_storage_secret" {
  template = <<EOF
apiVersion: v1
kind: Secret
metadata:
  creationTimestamp: null
  name: ${local.input.stage}-${local.input.project}-${local.input.component}-storage-secret
type: Opaque
stringData:
  azurestorageaccountname: ${azurerm_storage_account.this.name}
  azurestorageaccountkey: ${azurerm_storage_account.this.primary_access_key}
EOF
}

resource "local_file" "k8s_storage_secret" {
  content  = data.template_file.k8s_storage_secret.rendered
  filename = "../k8s/secret.yaml"
}

data "template_file" "k8s_storage_pv" {
  template = <<EOF
apiVersion: v1
kind: PersistentVolume
metadata:
  name: ${local.input.stage}-${local.input.project}-${local.input.component}-storage-pv
  labels:
    usage: ${local.input.stage}-${local.input.project}-${local.input.component}-storage-pv
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  azureFile:
    secretName: ${local.input.stage}-${local.input.project}-${local.input.component}-storage-secret
    shareName: ${azurerm_storage_share.this.name}
    readOnly: false
EOF
}

resource "local_file" "k8s_storage_pv" {
  content  = data.template_file.k8s_storage_pv.rendered
  filename = "../k8s/pv.yaml"
}

data "template_file" "k8s_storage_pvc" {
  template = <<EOF
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ${local.input.stage}-${local.input.project}-${local.input.component}-storage-pvc
  annotations:
    volume.beta.kubernetes.io/storage-class: ""
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 10Gi
  selector:
    matchLabels:
      usage: ${local.input.stage}-${local.input.project}-${local.input.component}-storage-pv
EOF
}

resource "local_file" "k8s_storage_pvc" {
  content  = data.template_file.k8s_storage_pvc.rendered
  filename = "../k8s/pvc.yaml"
}