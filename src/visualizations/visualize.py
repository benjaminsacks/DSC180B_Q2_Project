import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import pandas as pd
import os

font = {'family': 'DejaVu Sans',
        'weight': 'bold',
        'size': 15}


def make_folder(name):
    if not os.path.exists(name):
        os.makedirs(name)


def plot_classification(config, auroc, aupr):
    folder = "figures/" + config["experiment_name"]
    title = config["experiment_title"]
    make_folder(folder)
    file = folder + "/" + config["experiment_name"]
    plot_boxplot(title + " AUROC", file + "_AUROC.png", auroc)
    plot_boxplot(title + " AUPR", file + "_AUPR.png", aupr)


def plot_regression(config, mses):
    file = "figures/" + config["experiment_name"]
    title = config["experiment_title"]
    plot_boxplot(title + " MSE", file + "_MSE.png", mses)


def plot_boxplot(title, file_name, dict):
    data = list(dict.values())
    ticks = list(dict.keys())

    fig = plt.figure()
    ax = fig.add_axes([0.1, 0.1, 0.75, 0.75])
    ax.boxplot(data)
    ax.set_xticklabels(ticks)
    plt.title(title)
    plt.savefig(file_name)
    plt.close(fig)
    return plt


def plot_confidence_interval(x, values, z=1.96, color='#2187bb', horizontal_line_width=0.25):
    mean = np.mean(values)
    stdev = np.std(values)
    confidence_interval = z * stdev / (len(values) ** (1 / 2))

    left = x - horizontal_line_width / 2
    top = mean - confidence_interval
    right = x + horizontal_line_width / 2
    bottom = mean + confidence_interval
    plt.plot([x, x], [top, bottom], color=color)
    plt.plot([left, right], [top, top], color=color)
    plt.plot([left, right], [bottom, bottom], color=color)
    plt.plot(x, mean, 'o', color=color)

    # TODO: Delete this when plot_model_metrics() is rewritten
    plt.savefig('final_figure.png')

    return mean, confidence_interval


def init_visualization(cancer_stages):
    # INITIALIZE PLOT
    fig = plt.figure()
    y_ticks = plt.yticks(np.arange(11) / 10)
    x_ticks = plt.xticks(np.arange(1, len(cancer_stages.columns) + 1), [stage for stage in cancer_stages.columns])
    plt.autoscale(False)
    title = plt.title('AUROC')


def create_pca(data, targets, target_column):
    # idx = np.random.permutation(data.index)
    # data = data.reindex(idx)[:500]
    # targets = targets.reindex(idx)[:500]
    # # Run MDS
    # ## 
    # from sklearn.metrics import pairwise_distances
    # from sklearn.manifold import MDS

    # import warnings
    # from sklearn.exceptions import DataConversionWarning
    # warnings.filterwarnings(action='ignore', category=DataConversionWarning)

    # distance_metric = 'jaccard'

    # distances = pairwise_distances(data.to_numpy(), metric=distance_metric)
    # pd.DataFrame(distances).to_csv('distances.csv')
    # mds = MDS(dissimilarity='precomputed', random_state=0, normalized_stress=False)
    # pca_data = mds.fit_transform(distances)

    # Run PCA
    ## Standardize data
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)
    ## Run sklearn PCA on data
    pca = PCA(n_components=2)
    pca_data = pca.fit_transform(scaled_data)
    # Convert ndarray to DataFrame, Add targets back in
    pca_data = pd.DataFrame(pca_data, index=data.index)
    pca_data = pd.merge(pca_data, targets, on="sampleid", how="inner")

    # Plot PCA
    ## Create scatterplot

    sns.scatterplot(x=0, y=1, data=pca_data,
                    hue=target_column,
                    alpha=0.3)
    plt.title("PCoA")
    plt.legend(bbox_to_anchor=(1.01, 1),
               loc=2,
               borderaxespad=0.,
               title=target_column)
    ## Format PC labels to include explained variance
    plt.xlabel(f'PC1 ({round(pca.explained_variance_[0], 2)}%)')
    plt.ylabel(f'PC2 ({round(pca.explained_variance_[1], 2)}%)')
    ## Save fig
    plt.savefig("figures\pca\PCA_" + target_column + ".png", bbox_inches='tight')

    # Return loading scores
    ## Get loading scores from both PC's
    pc1_loading_scores = pd.Series(pca.components_[0], index=data.columns)
    pc2_loading_scores = pd.Series(pca.components_[1], index=data.columns)
    ## Sort loading scores by magnitude
    pc1_loading_scores = pc1_loading_scores.abs().sort_values(ascending=False)
    pc2_loading_scores = pc2_loading_scores.abs().sort_values(ascending=False)
    ## Return extracted series
    return pc1_loading_scores, pc2_loading_scores
