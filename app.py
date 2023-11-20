import streamlit as st
import pandas as pd
import mysql.connector

# Connect to the MySQL database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='shubhika',
    database='ShinjuBrews',
    port='3306'  # Replace with your actual MySQL port
)
cursor = conn.cursor()

# Function to fetch data from the database


def fetch_data(table_name):
    query = f"SELECT * FROM {table_name};"
    df = pd.read_sql(query, conn)
    return df

# Function to execute custom queries (INSERT, UPDATE, DELETE)


def execute_query(query):
    cursor.execute(query)
    conn.commit()


def fetch_correlated_data(selected_product):
    query = f"""
    SELECT PurchaseOrder.OrderID, PurchaseOrder.ProductID, Product.ProductName, PurchaseOrder.OrderDate, PurchaseOrder.ExpectedDeliveryDate, PurchaseOrder.Status, PurchaseOrder.totalAmount
    FROM PurchaseOrder
    JOIN Product ON PurchaseOrder.ProductID = Product.ProductID
    WHERE Product.ProductName = '{selected_product}';
    """
    df = pd.read_sql(query, conn)
    return df


def fetch_nested_data(selected_product):
    query = f"""
    SELECT Supplier.SupplierID, Supplier.SupplierName, Supplier.ContactInfo
    FROM Supplier
    WHERE Supplier.SupplierID IN (
        SELECT PurchaseOrder.SupplierID
        FROM PurchaseOrder
        JOIN Product ON PurchaseOrder.ProductID = Product.ProductID
        WHERE Product.ProductName = '{selected_product}'
    );
    """
    df = pd.read_sql(query, conn)
    return df

# Streamlit App


def main():
    st.title('ShinjuBrews Database App')

    # Sidebar options
    option = st.sidebar.radio('Select Option', [
                              'CRUD', 'Different types of queries', 'Procedures and Triggers'])

    # CRUD Operations
    if option == 'CRUD':
        st.subheader('Perform CRUD Operations on a Table:')
        selected_table = st.radio(
            'Select Table', ['Product', 'Supplier', 'PurchaseOrder', 'Customer'])
        st.subheader(f'Perform CRUD Operations on {selected_table} Table:')
        # Choose CRUD operation
        crud_operation = st.radio(
            'Choose Operation', ['Create', 'Read', 'Update', 'Delete'])

        # Display the selected operation
        st.write(f'Selected Operation: {crud_operation}')

        if crud_operation == 'Create':
            st.subheader(f'Add a New Record to {selected_table}:')
            if selected_table == 'Product':
                # Input fields for creating a new product
                product_id = st.number_input('ProductID', min_value=1, step=1)
                product_name = st.text_input('ProductName')
                description = st.text_area('Description')
                unit_price = st.number_input(
                    'UnitPrice', min_value=0.01, step=0.01)
                quantity_in_stock = st.number_input(
                    'QuantityInStock', min_value=0, step=1)

                if st.button(f'Add {selected_table}'):
                    execute_query(
                        f"INSERT INTO {selected_table} (ProductID, ProductName, Description, UnitPrice, QuantityInStock) VALUES ({product_id}, '{product_name}', '{description}', {unit_price}, {quantity_in_stock});")
                    st.success(f'New {selected_table} added!')

                    st.subheader(f'Current {selected_table} Table:')
                    updated_df = fetch_data(selected_table)
                    st.dataframe(updated_df)

            elif selected_table == 'Supplier':
                supplier_id = st.number_input(
                    'SupplierID', min_value=1, step=1)
                supplier_name = st.text_input('SupplierName')
                contact_info = st.text_area('ContactInfo')

                if st.button(f'Add {selected_table}'):
                    execute_query(
                        f"INSERT INTO {selected_table} (SupplierID, SupplierName, ContactInfo) VALUES ({supplier_id}, '{supplier_name}', '{contact_info}');")
                    st.success(f'New {selected_table} added!')

                    st.subheader(f'Current {selected_table} Table:')
                    updated_df = fetch_data(selected_table)
                    st.dataframe(updated_df)

            elif selected_table == 'PurchaseOrder':
                product_id = st.number_input('ProductID', min_value=1, step=1)
                order_id = st.number_input('OrderID', min_value=1, step=1)
                supplier_id = st.number_input(
                    'SupplierID', min_value=1, step=1)
                order_date = st.date_input('OrderDate')
                expected_delivery_date = st.date_input('ExpectedDeliveryDate')
                status = st.text_input('Status')
                total_amount = st.number_input(
                    'TotalAmount', min_value=0, step=1)

                if st.button(f'Add {selected_table}'):
                    execute_query(
                        f"INSERT INTO {selected_table} (ProductID, OrderID, SupplierID, OrderDate, ExpectedDeliveryDate, Status, totalAmount) VALUES ({product_id}, {order_id}, {supplier_id}, '{order_date}', '{expected_delivery_date}', '{status}', {total_amount});")
                    st.success(f'New {selected_table} added!')

                    st.subheader(f'Current {selected_table} Table:')
                    updated_df = fetch_data(selected_table)
                    st.dataframe(updated_df)

            elif selected_table == 'Customer':
                customer_id = st.number_input(
                    'CustomerID', min_value=1, step=1)
                first_name = st.text_input('FirstName')
                last_name = st.text_input('LastName')
                email = st.text_input('Email')
                phone_number = st.text_input('PhoneNumber')
                address = st.text_area('Address')

                if st.button(f'Add {selected_table}'):
                    execute_query(
                        f"INSERT INTO {selected_table} (CustomerID, FirstName, LastName, EMail, PhoneNumber, Address) VALUES ({customer_id}, '{first_name}', '{last_name}', '{email}', '{phone_number}', '{address}');")
                    st.success(f'New {selected_table} added!')

                    st.subheader(f'Current {selected_table} Table:')
                    updated_df = fetch_data(selected_table)
                    st.dataframe(updated_df)

        elif crud_operation == 'Read':
            # Display the updated table
            st.subheader(f'{crud_operation} {selected_table} Table:')
            updated_df = fetch_data(selected_table)
            st.dataframe(updated_df)

        elif crud_operation == 'Update':
            st.subheader(f'Update a Record in {selected_table} Table:')

            updated_df = fetch_data(selected_table)
            st.dataframe(updated_df)

            # Input field for specifying the ID to update
            record_id = st.number_input(
                f'{selected_table} ID to Update', min_value=1, step=1)

            # Get the list of column names for the selected table
            cursor.execute(f"DESCRIBE {selected_table};")
            columns = [column[0] for column in cursor.fetchall()]

            # Select the column to update
            selected_column = st.selectbox('Select Column to Update', columns)

            # Input field for the new value
            new_value = st.text_input(f'Enter New Value for {selected_column}')

            if st.button(f'Update {selected_table}'):
                # Execute the update query based on the specified ID and column
                execute_query(
                    f"UPDATE {selected_table} SET {selected_column} = '{new_value}' WHERE {selected_table}ID = {record_id};")
                st.success(
                    f'Record with {selected_table}ID {record_id} updated!')

                st.subheader(f'New {selected_table} Table:')
                updated_df = fetch_data(selected_table)
                st.dataframe(updated_df)

        elif crud_operation == 'Delete':
            st.subheader(f'Delete a Record from {selected_table}:')

            if selected_table == 'PurchaseOrder':
                st.warning(
                    "Cannot delete PurchaseOrder records. Use the 'Update' operation to change the status instead.")

            else:
                st.subheader(f'Current {selected_table} Table:')
                updated_df = fetch_data(selected_table)
                st.dataframe(updated_df)

                # Input field for specifying the ID to delete
                record_id = st.number_input(
                    f'{selected_table} ID to Delete', min_value=1, step=1)

                if st.button(f'Delete {selected_table}'):
                    # Execute the delete query based on the specified ID
                    execute_query(
                        f"DELETE FROM {selected_table} WHERE {selected_table}ID = {record_id};")
                    st.warning(
                        f'Record with {selected_table}ID {record_id} deleted!')

                    st.subheader(f'New {selected_table} Table:')
                    updated_df = fetch_data(selected_table)
                    st.dataframe(updated_df)

    # Different types of queries
    elif option == 'Different types of queries':
        # st.subheader('Choose a Table for Query:')
        # selected_table_query = st.radio(
        #     'Select Table', ['Product', 'Supplier', 'PurchaseOrder', 'Customer'])

        # Dropdown menu for product selection
        product_options = ['Classic Milk Tea', 'Taro', 'Matcha']
        selected_product = st.selectbox('Select Product:', product_options)

        st.title('Correlated Query')

        # Display correlated data for the selected product
        st.subheader(f'Purchase Orders for {selected_product}:')
        correlated_data = fetch_correlated_data(selected_product)
        st.dataframe(correlated_data)

        st.title('Nested Query')

        # Dropdown menu for product selection
        # product_options = ['Classic Milk Tea', 'Taro', 'Matcha']
        # selected_product = st.selectbox('Select Product:', product_options)

        # Display nested data for the selected product
        st.subheader(f'Suppliers for {selected_product}:')
        nested_data = fetch_nested_data(selected_product)
        st.dataframe(nested_data)

    # Procedures and Triggers
    elif option == 'Procedures and Triggers':
        st.title('Stored Procedure:')
        st.subheader(
            "Whatever Product you choose, the Stored Procedure will fetch it's Purchase Orders.")
        # selected_table_procedure_trigger = st.radio(
        #     'Select Table', ['Product', 'Supplier', 'PurchaseOrder', 'Customer'])
        # # Dropdown menu for product selection
        product_options = ['Classic Milk Tea', 'Taro', 'Matcha']
        selected_product = st.selectbox('Select Product:', product_options)

        # Button to call the stored procedure
        if st.button('Get Purchase Orders'):
            # Call the stored procedure
            cursor.callproc('GetPurchaseOrdersForProduct', (selected_product,))

            # Fetch the results
            for result in cursor.stored_results():
                purchase_orders = result.fetchall()

            # Display the results in a DataFrame
            if purchase_orders:
                columns = ["OrderID", "OrderDate",
                           "ExpectedDeliveryDate", "Status", "ProductName"]
                df = pd.DataFrame(purchase_orders, columns=columns)
                st.subheader(f'Purchase Orders for {selected_product}:')
                st.dataframe(df)
            else:
                st.warning(f'No purchase orders found for {selected_product}.')

        st.title('Trigger:')
        st.subheader(
            "Whenever you add a new Purchase Order, using Trigger, it's quantity in stock is increased by that amount.")
        product_id = st.number_input('ProductID', min_value=1, step=1)
        order_id = st.number_input('OrderID', min_value=1, step=1)
        supplier_id = st.number_input('SupplierID', min_value=1, step=1)
        order_date = st.date_input('OrderDate')
        expected_delivery_date = st.date_input('ExpectedDeliveryDate')
        status = st.text_input('Status')
        total_amount = st.number_input('TotalAmount', min_value=0, step=1)

        if st.button(f'Add Purchase Order'):
            execute_query(
                f"INSERT INTO PurchaseOrder (ProductID, OrderID, SupplierID, OrderDate, ExpectedDeliveryDate, Status, totalAmount) VALUES ({product_id}, {order_id}, {supplier_id}, '{order_date}', '{expected_delivery_date}', '{status}', {total_amount});")
            st.success(f'New PurchaseOrder added!')

            st.subheader(f'Current PurchaseOrder Table:')
            updated_df = fetch_data("PurchaseOrder")
            st.dataframe(updated_df)

            st.subheader(f'Product Table:')
            updated_df = fetch_data('Product')
            st.dataframe(updated_df)


if __name__ == '__main__':
    main()
