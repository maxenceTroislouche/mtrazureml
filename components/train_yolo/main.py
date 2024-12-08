import argparse
from pathlib import Path
from ultralytics import YOLO


def train_yolo(data_yaml: str, model_name: str, epochs: int, img_size: int, output_dir: str):
    """
    Entraîne un modèle YOLO sur le dataset Waldone.

    Args:
        data_yaml (str): Chemin vers le fichier YAML décrivant les données.
        model_name (str): Nom du modèle YOLO pré-entraîné à utiliser (par ex. 'yolov5s').
        epochs (int): Nombre d'époques d'entraînement.
        img_size (int): Taille des images utilisées pour l'entraînement.
        output_dir (str): Répertoire pour enregistrer les résultats de l'entraînement.
    """
    if not Path(data_yaml).exists():
        raise FileNotFoundError(f"Le fichier de configuration des données '{data_yaml}' est introuvable.")

    model = YOLO(model_name)  # Charge le modèle pré-entraîné
    model.train(data=data_yaml, epochs=epochs, imgsz=img_size, project=output_dir)

    return model


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_dir", type=str, required=True, help="Répertoire de sortie pour le modèle")
    args = parser.parse_args()

    # Exemple d'utilisation
    train_yolo(
        data_yaml="datasets/data.yaml",
        model_name="yolov8n.pt",
        epochs=10,
        img_size=640,
        output_dir=args.output_dir
    )
