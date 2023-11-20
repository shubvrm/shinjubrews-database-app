CREATE DATABASE ShinjuBrews;
USE ShinjuBrews;

-- Create the Product table
CREATE TABLE Product (
    ProductID INT PRIMARY KEY,
    ProductName VARCHAR(255),
    Description TEXT,
    UnitPrice DECIMAL(10, 2),
    QuantityInStock INT
);

-- Create the Supplier table 
CREATE TABLE Supplier (
    SupplierID INT PRIMARY KEY,
    SupplierName VARCHAR(255),
    ContactInfo TEXT,
    SuppliedProducts TEXT
);

-- Create the PurchaseOrder table
CREATE TABLE PurchaseOrder (
    ProductID INT,
    OrderID INT PRIMARY KEY,
    SupplierID INT,
    OrderDate DATE,
    ExpectedDeliveryDate DATE,
    Status VARCHAR(50),
    totalAmount INT,
    FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID)
);

CREATE TABLE Customer (
    CustomerID INT PRIMARY KEY,
    FirstName VARCHAR(20),
    LastName VARCHAR(20),
    EMail VARCHAR(20),
    PhoneNumber VARCHAR(10),
    Address VARCHAR(50)
);


-- Insert data into the Product table
INSERT INTO Product (ProductID, ProductName, Description, UnitPrice, QuantityInStock)
VALUES
    (1, 'Classic Milk Tea', 'Made with black tea and milk, often sweetened with sugar or condensed milk.', 4.99, 50),
    (2, 'Taro', 'Made with taro root to create a creamy and slightly sweet flavor.', 5.49, 40),
    (3, 'Matcha', 'Made with high-quality green tea powder, has a distinct earthy and slightly bitter taste.', 6.99, 30);


-- Insert data into the Supplier table
INSERT INTO Supplier (SupplierID, SupplierName, ContactInfo)
VALUES
    (1, 'Fruit Syrup Co.', 'info@fruitsyrupcompany.com'),
    (2, 'Coffee Beans Inc.', 'sales@coffeebeansinc.com'),
    (3, 'Honeydew Farms', 'orders@honeydewfarms.com');

-- Inserting records into the PurchaseOrder table
INSERT INTO PurchaseOrder (ProductID, OrderID, SupplierID, OrderDate, ExpectedDeliveryDate, Status, totalAmount)
VALUES
    (1, 101, 1, '2023-11-17', '2023-11-25', 'Pending', 500),
    (2, 102, 2, '2023-11-18', '2023-11-26', 'Processing', 700),
    (3, 103, 3, '2023-11-19', '2023-11-27', 'Shipped', 1000);

-- Inserting records into the Customer table
INSERT INTO Customer (CustomerID, FirstName, LastName, EMail, PhoneNumber, Address)
VALUES
    (1, 'John', 'Doe', 'john.doe@ex.com', '1234567890', '123 Main St'),
    (2, 'Jane', 'Smith', 'jane.smith@ex.com', '9876543210', '456 Oak St'),
    (3, 'Bob', 'Johnson', 'bob.johnson@ex.com', '5555555555', '789 Maple St');

-- Procedure to obtain PurchaseOrders from Product Name
DELIMITER //
CREATE PROCEDURE GetPurchaseOrdersForProduct(IN product_name VARCHAR(255))
BEGIN
    SELECT PurchaseOrder.OrderID, PurchaseOrder.OrderDate, PurchaseOrder.ExpectedDeliveryDate, PurchaseOrder.Status, Product.ProductName
    FROM PurchaseOrder
    JOIN Product ON PurchaseOrder.ProductID = Product.ProductID
    WHERE Product.ProductName = product_name;
END //
DELIMITER ;

-- Trigger to update QuantityInStock when new PurchaseOrder is added
DELIMITER //
CREATE TRIGGER AfterPurchaseOrderInsert
AFTER INSERT
ON PurchaseOrder FOR EACH ROW
BEGIN
    DECLARE product_quantity INT;
    SELECT QuantityInStock INTO product_quantity FROM Product WHERE ProductID = NEW.ProductID;
    UPDATE Product SET QuantityInStock = product_quantity + NEW.totalAmount WHERE ProductID = NEW.ProductID;
END //
DELIMITER ;
